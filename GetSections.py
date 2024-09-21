from testrail_api import TestRailAPI
import requests
from operator import itemgetter
import operator

username = 'daniel.brym@eftlab.com'
password = '8PHo0GxLkcG2SKSM8EZL-N0bxD3gQMy3g17y.lOk6'


def get_sections(sections_url):
    url=sections_url
    list_sects = []
    while url:
        response = requests.get(url, auth=(username, password))
        data=response.json()
        all_sections=data['sections']
        for i in range(len(all_sections)):
            sections_depth = all_sections[i]['depth']
            sections_id = all_sections[i]['id']
            secions_name = all_sections[i]['name']
            #print("id: ", sections_id, "name: ", secions_name, " depth: ", sections_depth)
            list_sects.append([{'id': sections_id, 'name': secions_name}])

        if data['_links']['next'] is not None:
            url='https://eftlab.testrail.io/index.php?'+data['_links']['next']
        else:
            break
    return list_sects


def get_all_sections(json_url,project_id,sections=False,sub_sections=False,sub_of_sub_sections=False):
    api = TestRailAPI(json_url, username, password)
    response = api.get('get_sections/' + str(project_id))
    response['sections'].sort(key=lambda x: int(x['id']), reverse=True)
    all_sections=response['sections']
    print("reversed: ",all_sections)
    list_sects=[]
    for i in range(len(all_sections['sections'])):
        sections_depth = all_sections['sections'][i]['depth']
        sections_id = all_sections['sections'][i]['id']
        secions_name = all_sections['sections'][i]['name']

        # print("id: ", sections_id, "name: ", secions_name, " depth: ", sections_depth)
        # list_sects.append([{'id': sections_id, 'name': secions_name}])

        if sub_of_sub_sections or (sub_sections and sub_of_sub_sections) or (sections and sub_sections and sub_of_sub_sections) or (sections and sub_of_sub_sections):
            if sections_depth == 1 or sections_depth==0 or sections_depth==2 or sections_depth==3 or sections_depth==4:
                print("id: ", sections_id, " name: ", secions_name,"depth: ",sections_depth)
                list_sects.append([{'id': sections_id, 'name': secions_name}])
        elif (sections and sub_sections) or (not sections and sub_sections):
            if sections_depth == 1 or sections_depth==0:
                print("id: ", sections_id, " name: ", secions_name,"depth: ",sections_depth)
                list_sects.append([{'id': sections_id, 'name': secions_name}])
        elif (sections and not sub_sections and not sub_of_sub_sections):
            if sections_depth==0:
                print("id: ", sections_id, " name: ", secions_name,"depth: ",sections_depth)
                list_sects.append([{'id': sections_id, 'name': secions_name}])
        else:
            print("id: ", sections_id, " name: ", secions_name, "depth: ", sections_depth)
            list_sects.append([{'id': sections_id, 'name': secions_name}])
    if all_sections['_links']['next'] is not None:
        next_url=all_sections['_links']['next']
        while next_url is not None:
            api_temp=TestRailAPI(json_url, username, password)
            next_url = next_url.strip('/api/v2/')
            next_url_temp = api_temp.get(next_url)
            for i in range(len(next_url_temp['sections'])):
                sections_depth = next_url_temp['sections'][i]['depth']
                sections_id = next_url_temp['sections'][i]['id']
                secions_name = next_url_temp['sections'][i]['name']
                # print("id: ",sections_id,"name: ",secions_name," depth: ",sections_depth)
                # list_sects.append([{'id': sections_id, 'name': secions_name}])
                if sub_of_sub_sections or (sub_sections and sub_of_sub_sections) or (
                        sections and sub_sections and sub_of_sub_sections) or (sections and sub_of_sub_sections):
                    if sections_depth == 1 or sections_depth == 0 or sections_depth == 2 or sections_depth == 3 or sections_depth == 4:
                        print("id: ", sections_id, " name: ", secions_name, "depth: ", sections_depth)
                        list_sects.append([{'id': sections_id, 'name': secions_name}])
                elif (sections and sub_sections) or (not sections and sub_sections):
                    if sections_depth == 1 or sections_depth == 0:
                        print("id: ", sections_id, " name: ", secions_name, "depth: ", sections_depth)
                        list_sects.append([{'id': sections_id, 'name': secions_name}])
                elif (sections and not sub_sections and not sub_of_sub_sections):
                    if sections_depth == 0:
                        print("id: ", sections_id, " name: ", secions_name, "depth: ", sections_depth)
                        list_sects.append([{'id': sections_id, 'name': secions_name}])
                else:
                    print("id: ", sections_id, " name: ", secions_name, "depth: ", sections_depth)
                    list_sects.append([{'id': sections_id, 'name': secions_name}])
            next_url=all_sections['_links']['next']
            if next_url is not None:
                next_url=next_url
                print("next page: ",next_url)

    return list_sects


def create_section(json_url,project_id, section_id, title):
    endpoint = json_url+'/index.php?/api/v2/add_section/'+str(project_id)

    data = {
        'name': title,
        'parent_id': section_id
    }

    response = requests.post(
        endpoint,
        auth=(username,password),
        json=data
    )

    if response.status_code == 200:
        print('Section created with the name: ',title)
        return response.json()
    else:
        print(f'Failed to create section: {response.status_code}')
        print(response.text)
        return None


def create_test_case(json_url,section_id, testcase_name, template_id=1):
    endpoint = json_url+'/index.php?/api/v2/add_case/'+str(section_id)
    data = {
        'title': testcase_name,
        'template_id': template_id
    }
    response = requests.post(
        endpoint,
        auth=(username, password),
        json=data
    )
    if response.status_code == 200:
        print('Test case created with the name: ',testcase_name)
        return response.json()
    else:
        print(f'Failed to create test case: {response.status_code}')
        print(response.text)
        return None


if __name__ == "__main__":
    project_id = 1  # default
    section = True
    sub_section=True
    sub_of_sub_sections = True
    json_url = 'https://eftlab.testrail.io'
    sections_url='https://eftlab.testrail.io/index.php?/api/v2/get_sections/'+ str(project_id)

    # folder_names_list=['CMS', 'MCMIP']
    # subfolder_list=['01.0 0200 Preauthorication- Dodelat', '01.1 0200 Authorization']
    # testcases_list=[['0.01.Preauthorization-Cancellation','0.02.Preauthorization-Fallback','0.03.Preauthorization-ICC','0.04.Preauthorization-Band input track 2 complete','0.05.Preauthorization-mag stripe'],['1.01.Authorization-Magnetic Band']]

    folder_names_list = ['CMO-BNC', 'CMO-BPSMSAcq', 'CMO-CMS', 'CMO-MCMIP','MCMIP-Banplus', 'MCMIP-CMS']
    subfolder_list = ['01.0 0200 Preauthorication- Dodelat', '01.1 0200 Authorization', '01.3 0200 Credit Purchase','01.7 0200 Refund', '02.0 0400 Reversal', '03.0 0500 Batch cutover', '07.0 DE04', '08.0 DE07','09.0 DE11', '10.0 DE12', '11.0 DE13', '14.0 DE22', '15.0 DE23', '16.0 DE25', '18.0 DE32','19.0 DE35', '20.0 DE37', '22.0 DE39', '24.0 DE42', '25.0 DE46', '27.0 DE49', '28.0 DE52','29.0 DE43', '31.0 DE55', '32.0 DE56', '37.0 DE59', '38.0 DE24', '39.0 DE41', '40.0 DE47','41.0 DE62', '42.0 DE63', '44.0 DE03', '45.0 DE06', '46.0 DE15', '47.0 DE18', '49.0 DE33','50.0 DE50', '51.0 DE51', '52.0 DE61_Banplus', '53.0 Format errors', '54.0 MAC Error','55.0 Timeout', '56.0 DE122']
    testcases_list=[['0.01.Preauthorization-Cancellation','0.02.Preauthorization-Fallback','0.03.Preauthorization-ICC','0.04.Preauthorization-Band input track 2 complete','0.05.Preauthorization-mag stripe'],['1.01.Authorization-Magnetic Band','1.02.Authorization-Fallback','1.03.Authorization-ICC','1.04.Authorization-Band input track 2 complete'],['3.01.Credit Purchase-Magnetic Band','3.02 Credit Purchase-fallback','3.03.Credit Purchase-ICC','3.04.Credit Purchase-Band input track 2 complete'],['7.02.Refund-fallback','7.03.Refund-ICC','7.04.Refund-Band input track 2 complete','7.05.Refund-Magnetic Band'],['02.01 Authorization Reversal','02.02 Reversal with no original Authorization'],['1500 Subtotals with credit-credit reversal','1500 subtotals with debit-debit reversal','1520 Settlement out of balance','1520 Settlement with credit-credit reversal','1520 Settlement with debit-debit reversal','3.01.Batch cutover-out of balance'],['7.01.Authorization.DE04.0000','7.02.Authorization.DE04.0001','7.03.Authorization.DE04.0100','7.04.Authorization.DE04.9999999'],['08.01.200.DE07.1015233059'],['9.01.Authorization.DE11.123456'],['10.01.Authorization.DE12.220059'],['11.01.Authorization.DE13.1015'],['14.02.021','14.02.812','14.03.051','14.04.801','14.05.901','14.06.000','14.07.502'],['15.01.Authorization.DE23.001','15.02.Authorization.DE23.999','15.01.Authorization.DE23.123'],['16.01.Authorization.DE25.00'],['18.01.Authorization.DE32.0001'],['19.01.Authorization.DE35'],['20.01.Authorization.DE37.000000001973'],['22.01.DE39.00-00','22.01.DE39.01-01','22.01.DE39.03-03','22.01.DE39.04-04','22.01.DE39.05-05','22.01.DE39.06-06','22.01.DE39.08-08','22.01.DE39.10-00','22.01.DE39.15-15','22.01.DE39.12-12','22.01.DE39.13.13','22.01.DE39.14-14','22.01.DE39.16-00','22.01.DE39.17-17','22.01.DE39.25-25','22.01.DE39.26-26','22.01.DE39.27-27','22.01.DE39.28-28','22.01.DE39.29-29','22.01.DE39.30-30','22.01.DE39.34-34','22.01.DE39.40-40','22.01.DE39.41-41','22.01.DE39.43-43','22.01.DE39.51-51','22.01.DE39.54-54','22.01.DE39.55-55','22.01.DE39.57-57','22.01.DE39.58-58','22.01.DE39.61-61','22.01.DE39.62-62','22.01.DE39.63-63','22.01.DE39.65-65','22.01.DE39.68-68','22.01.DE39.70-70','22.01.DE39.71-71','22.01.DE39.75-75','22.01.DE39.76-76','22.01.DE39.78-78','22.01.DE39.79-79','22.01.DE39.80-80','22.01.DE39.81-81','22.01.DE39.82-82','22.01.DE39.84-84','22.01.DE39.85-85','22.01.DE39.86-86','22.01.DE39.87-87','22.01.DE39.88-88','22.01.DE39.89-05','22.01.DE39.91-91','22.01.DE39.92-92','22.01.DE39.94-94','22.01.DE39.96-96'],['24.01.Authorization.DE42.42298501010101'],['25.01.Authorization.DE46'],['27.001.Authorization.ALL.008','27.001.Authorization.DZD.012','27.001.Authorization.ARS.032','27.001.Authorization.AUD.036','27.001.Authorization.BSD.044','27.001.Authorization.BHD.048','27.001.Authorization.BDT.050','27.001.Authorization.AMD.051','27.001.Authorization.BBD.052','27.001.Authorization.BMD.052','27.001.Authorization.BTN.064','27.001.Authorization.BOB.068','27.001.Authorization.BWP.072','27.001.Authorization.BZD.084','27.001.Authorization.SBD.090','27.001.Authorization.BND.084','27.001.Authorization.MMK.104','27.001.Authorization.BIF.108','27.001.Authorization.KHR.116','27.001.Authorization.CAD.124','27.001.Authorization.CVE.132','27.001.Authorization.KYD.136','27.001.Authorization.LKR.144','27.001.Authorization.CLP.152','27.001.Authorization.CNY.156','27.001.Authorization.COP.170','27.001.Authorization.KMF.174','27.001.Authorization.CRC.188','27.001.Authorization.HRK.191','27.001.Authorization.CUP.192','27.001.Authorization.CZK.203','27.001.Authorization.DKK.208','27.001.Authorization.DOP.214','27.001.Authorization.SVC.222','27.001.Authorization.ETB.230','27.001.Authorization.ERN.232','27.001.Authorization.FKP.238','27.001.Authorization.FJD.242','27.001.Authorization.DJF.262','27.001.Authorization.GMD.270','27.001.Authorization.GIP.292','27.001.Authorization.GTQ.320','27.001.Authorization.GNF.324','27.001.Authorization.GYD.328','27.001.Authorization.HTG.332','27.001.Authorization.HNL.340','27.001.Authorization.HKD.344','27.001.Authorization.HUF.348','27.001.Authorization.ISK.352','27.001.Authorization.INR.356','27.001.Authorization.IDR.360','27.001.Authorization.IRR.364','27.001.Authorization.IQD.368','27.001.Authorization.ILS.376','27.001.Authorization.JMD.388','27.001.Authorization.JPY.392','27.001.Authorization.KZT.398','27.001.Authorization.JOD.400','27.001.Authorization.KES.404','27.001.Authorization.KPW.408','27.001.Authorization.KRW.410','27.001.Authorization.KWD.414','27.001.Authorization.KGS.417','27.001.Authorization.LAK.418','27.001.Authorization.LBP.422','27.001.Authorization.LSL.426','27.001.Authorization.LRD.430','27.001.Authorization.LYD.430','27.001.Authorization.MOP.466','27.001.Authorization.MWK.454','27.001.Authorization.MYR.458','27.001.Authorization.MVR.462','27.001.Authorization.MUR.480','27.001.Authorization.MXN.484','27.001.Authorization.MNT.496','27.001.Authorization.MDL.498','27.001.Authorization.MAD.504','27.001.Authorization.OMR.512','27.001.Authorization.NAD.516','27.001.Authorization.NPR.524','27.001.Authorization.ANG.532','27.001.Authorization.AWG.533','27.001.Authorization.VUV.548','27.001.Authorization.NZD.554','27.001.Authorization.NIO.558','27.001.Authorization.NGN.566','27.001.Authorization.NOK.578','27.001.Authorization.PKR.586','27.001.Authorization.PAB.590','27.001.Authorization.PGK.598','27.001.Authorization.PYG.600','27.001.Authorization.PEN.604','27.001.Authorization.PHP.608','27.001.Authorization.QAR.634','27.001.Authorization.RUB.643','27.001.Authorization.RWF.646','27.001.Authorization.SHP.654','27.001.Authorization.SAR.682','27.001.Authorization.SCR.690','27.001.Authorization.SLL.694','27.001.Authorization.SGD.702','27.001.Authorization.VND.704','27.001.Authorization.SOS.706','27.001.Authorization.ZAR.710','27.001.Authorization.SSP.728','27.001.Authorization.SZL.748','27.001.Authorization.SEK.752','27.001.Authorization.CHF.756','27.001.Authorization.SYP.760','27.001.Authorization.THB.764','27.001.Authorization.TOP.776','27.001.Authorization.TTD.780','27.001.Authorization.AED.784','27.001.Authorization.TND.784','27.001.Authorization.UGX.800','27.001.Authorization.MKD.807','27.001.Authorization.EGP.818','27.001.Authorization.GBP.826','27.001.Authorization.TZS.834','27.001.Authorization.USD.840','27.001.Authorization.UYU.858','27.001.Authorization.UZS.860','27.001.Authorization.WST.882','27.001.Authorization.YER.886','27.001.Authorization.TWD.901','27.001.Authorization.UYW.927','27.001.Authorization.VES.928','27.001.Authorization.MRU.929','27.001.Authorization.STN.930','27.001.Authorization.CUC.931','27.001.Authorization.ZWL.932','27.001.Authorization.BYN.933','27.001.Authorization.TMT.934','27.001.Authorization.GHS.936','27.001.Authorization.SDG.938','27.001.Authorization.UYI.940','27.001.Authorization.RSD.941','27.001.Authorization.MZN.943','27.001.Authorization.AZN.944','27.001.Authorization.RON.946','27.001.Authorization.CHE.947','27.001.Authorization.TRY.949','27.001.Authorization.XAF.950','27.001.Authorization.XCD.951','27.001.Authorization.XOF.952','27.001.Authorization.XPF.953','27.001.Authorization.XBA.955','27.001.Authorization.XBB.956','27.001.Authorization.XBC.957','27.001.Authorization.XBD.958','27.001.Authorization.XAU.959','27.001.Authorization.XDR.960','27.001.Authorization.XAG.961','27.001.Authorization.XPT.962','27.001.Authorization.XTS.963','27.001.Authorization.XPD.964','27.001.Authorization.XUA.965','27.001.Authorization.ZMW.967','27.001.Authorization.SRD.968','27.001.Authorization.MGA.969','27.001.Authorization.COU.970','27.001.Authorization.AFN.971','27.001.Authorization.TJS.972','27.001.Authorization.AOA.973','27.001.Authorization.BGN.975','27.001.Authorization.CDF.976','27.001.Authorization.BAM.977','27.001.Authorization.EUR.978','27.001.Authorization.MXV.979','27.001.Authorization.UAH.980','27.001.Authorization.GEL.981','27.001.Authorization.BOV.984','27.001.Authorization.PLN.985','27.001.Authorization.BRL.986','27.001.Authorization.CLF.990','27.001.Authorization.XSU.994','27.001.Authorization.USN.997','27.001.Authorization.XXX.999'],['28.01.Authorization.DE52.7059EB34EOD5E2EF','28.02.Authorization.DE52.7059EB34EOD5E2E0'],['29.01.Authorization.DE43'],['31.01.Authorization.DE55.Request'],['32.01.Authorization.DE56.BSS'],['37.01.Authorization.DE59.D00000073280'],['38.01.Authorization.DE24.036'],['39.01.Authorization.DE41'],['40.01.Authorization.DE47'],['41.01.Authorization.DE62.001973'],['42.01.Authorization.DE63.00000012345678'],['44.01. DE03','44.02. DE03_024000'],['45.01 DE06'],['46.01 DE15'],['47.01 DE18'],['49.01 DE33'],['50.01 DE50'],['51.01 DE51'],['52.01 DE61.10_0','52.02 DE61.10_1','52.03 DE61.10_2','52.03 DE61.10_3','52.03 DE61.10_4','52.03 DE61.10_5','52.03 DE61.10_6','52.03 DE61.10_7','52.03 DE61.10_8','52.03 DE61.10_9','52.03 DE61.11_0','52.03 DE61.11_1','52.03 DE61.11_2','52.03 DE61.11_3','52.03 DE61.11_4','52.03 DE61.11_5','52.03 DE61.11_6','52.03 DE61.11_7','52.03 DE61.11_8','52.03 DE61.11_9','52.03 DE61.12_00','52.03 DE61.12_01','52.03 DE61.1_0','52.03 DE61.1_2','52.03 DE61.2','52.03 DE61.3_0','52.03 DE61.3_1','52.03 DE61.3_2','52.03 DE61.3_3','52.03 DE61.3_4','52.03 DE61.3_8','52.03 DE61.4_0','52.03 DE61.4_1','52.03 DE61.4_2','52.03 DE61.4_3','52.03 DE61.4_4','52.03 DE61.4_5','52.03 DE61.5_0','52.03 DE61.5_1','52.03 DE61.6_0','52.03 DE61.6_1','52.03 DE61.7_0','52.03 DE61.7_1','52.03 DE61.7_2','52.03 DE61.7_3','52.03 DE61.7_4','52.03 DE61.7_5','52.03 DE61.7_6','52.03 DE61.7_7','52.03 DE61.7_8','52.03 DE61.7_9','52.03 DE61.8_0','52.03 DE61.8_1','52.03 DE61.8_2','52.03 DE61.9_0'],['53.01 DE12 error','53.02 DE22 error','53.03 DE24 error','53.04 DE25 error','53.05 DE28 error','53.06 DE29 error','53.07 DE3 error','53.08 DE4 error','53.09 DE49 error','53.10 DE7 error','53.11 TID does not exists'],['1500','1520','54.01 1100','54.02 1200','54.03 1220'],['55.01 Issuer Timeout'],['56.0 DE122_001001','56.0 DE122_001002','56.0 DE122_001003','56.0 DE122_001004','56.0 DE122_01005','56.0 DE122_01006','56.0 DE122_01007','56.0 DE122_01008','56.0 DE122_01009','56.0 DE122_01010','56.0 DE122_01011','56.0 DE122_01012']]

    for i in range(len(folder_names_list)):
        #print("head name: ",folder_names_list[0])
        create_section(json_url, project_id, 121, folder_names_list[0])
        for j in range(0,len(subfolder_list)):
            #print("folder name: ",subfolder_list[j])
            sections_list = get_sections(sections_url)
            sections_list.sort(key=lambda x: int(x[0]['id']), reverse=True)
            for sec_id in range(len(sections_list)):
                section_name_temp = sections_list[sec_id][0]['name']
                if folder_names_list[0] == section_name_temp:
                    section_id_temp = sections_list[sec_id][0]['id']
                    create_section(json_url,project_id,section_id_temp,subfolder_list[j])
                    sections_list_sub=get_sections(sections_url)
                    sections_list_sub.sort(key=lambda x: int(x[0]['id']), reverse=True)
                    for sec_id_sub in range(len(sections_list_sub)):
                        section_name_temp_temp = sections_list_sub[sec_id_sub][0]['name']
                        if subfolder_list[j] == section_name_temp_temp:
                            section_id = sections_list_sub[sec_id_sub][0]['id']
                            print("section id: ",section_id," name: ",section_name_temp_temp)
                            if j < len(testcases_list):
                                for k in range(len(testcases_list[j])):
                                    create_test_case(json_url, section_id, testcases_list[j][k])
                                break

        del folder_names_list[0]





# folder_names_list = ['CMO-Banplus','CMO-BanplusMaestro','CMO-BNC','CMO-BPSMSAcq','CMO-CMS','CMO-MIPAcq','MCMIP-Banplus','MCMIP-CMS']
    #
    # testcases_list=[['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout','56.0 DE122'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout','56.0 DE122'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout','56.0 DE122'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout','56.0 DE122'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','05.0 0800 Network management','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout'],
    #                 ['01.0 0200 Preauthorication- Dodelat','01.1 0200 Authorization','01.3 0200 Credit Purchase','01.5 0200 C2P','01.7 0200 Refund','02.0 0400 Reversal','03.0 0500 Batch cutover','05.0 0800 Network management','07.0 DE04','08.0 DE07','09.0 DE11','10.0 DE12','11.0 DE13','14.0 DE22','15.0 DE23','16.0 DE25','18.0 DE32','19.0 DE35','20.0 DE37','22.0 DE39','24.0 DE42','25.0 DE46','27.0 DE49','28.0 DE52','29.0 DE43','31.0 DE55','32.0 DE56','37.0 DE59','38.0 DE24','39.0 DE41','40.0 DE47','41.0 DE62','42.0 DE63','44.0 DE03','45.0 DE06','46.0 DE15','47.0 DE18','49.0 DE33','50.0 DE50','51.0 DE51','52.0 DE61_Banplus','53.0 Format errors','54.0 MAC Error','55.0 Timeout']]
    #
    #
    # for i in range(len(folder_names_list)):
    #     if len(folder_names_list) >0:
    #         print("folder length: ", len(folder_names_list))
    #         section_name = folder_names_list[0]
    #         #print("folder name: ", section_name)
    #         sec_result = create_section(json_url, project_id, 121,
    #                                     section_name)  # create a section with the folder/section names
    #         if sec_result is not None:
    #             sections_list = get_all_sections(json_url, project_id, section, sub_section, sub_of_sub_sections)
    #             for sec_id in range(len(sections_list)):
    #                 section_name_temp = sections_list[sec_id][0]['name']
    #                 # print("section name in  list: ", section_name_temp)
    #                 if section_name in section_name_temp:
    #                     section_id = sections_list[sec_id][0]['id']
    #                     if i <= len(testcases_list):
    #                         current_testcases = testcases_list[0]
    #                         for testcase in current_testcases:
    #                             #print("testcase name: ", testcase)
    #                             create_test_case(json_url, section_id, testcase)
    #                         del testcases_list[0]
    #                         del folder_names_list[0]
    #                         break
    #










    # sections_list = get_all_sections(json_url, project_id,section,sub_section)
    #
    # for sec_id in range(len(sections_list)):
    #     section_name = sections_list[sec_id][0]['name']
    #     print("section name in collected list: ", section_name)
    #
    #     if 'ETA Orionis' in section_name:
    #         section_id = sections_list[sec_id][0]['id']
    #         print('section id of ETA orionis: ', section_id)
    #         for i in range(len(folder_names_list)):
    #             section_name=folder_names_list[i]
    #             print("folder name: ",section_name)
    #             for i in range(len(folder_names_list)):
    #                 section_name = folder_names_list[i]
    #                 sec_result=create_section(json_url, project_id, section_id, section_name)
    #                 if sec_result is not None:
    #                     if i <= len(testcases_list):
    #                         current_testcases = testcases_list[0]
    #                         for testcase in current_testcases:
    #                             print("testcase name: ", testcase)
    #                             create_test_case(json_url,section_id, testcase)
    #                         del testcases_list[0]
    #         break
    #











# create_test_case(json_url,section_id,testcase_name)






