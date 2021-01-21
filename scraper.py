#maruti suzuki remains, id = 38
for make_dict in tqdm(make_list[39:]):
    # print(make_dict)
    make = make_dict['value'].split()
    make = '+'.join(make)
    make_id = make_dict['data-make-id']
    getModelList = 'https://droom.in/getRepairServiceModelList?make='+make+'&make_id='+make_id+'&bucket=cars'
    # print(make, make_id)
    model_call = requests.get(getModelList, headers = headers)
    model_response = model_call.content
    model_list = json.loads(model_response.decode('utf-8'))['data']
    for model_dict in tqdm(model_list):
        model = model_dict['model_org_name'].split()
        model = '+'.join(model)
        model_id = model_dict['model_id']
        # print(make, make_id, model, model_id)
        getTrimList = "https://droom.in/getRepairServiceTrimList?make="+make+"&make_id="+make_id+"&model="+model+"&model_id="+model_id+"&bucket=cars"
        # print(getTrimList)
        model_call = requests.get(getTrimList, headers = headers)
        trim_response = model_call.content
        trim_list = json.loads(trim_response.decode('utf-8'))['data']
        for trim_dict in tqdm(trim_list):
            if 'trim_org_name' in trim_dict.keys():
                trim = trim_dict['trim_org_name'].split()
                trim = '+'.join(trim)
                trim_id = trim_dict['trim_id']
                if trim_id != '':
                    print(make, make_id, model, model_id, trim, trim_id)
                    getTrimDetails = "https://droom.in/getRepairServiceTrimDetails?make="+make+"&make_id="+make_id+"&model="+model+"&model_id="+model_id+"&bucket=cars&trim="+trim+"&trim_id="+trim_id
                    # print(getTrimDetails)
                    model_call = requests.get(getTrimDetails, headers = headers)
                    service_response = model_call.content
                    service_dict = json.loads(service_response.decode('utf-8'))
                    if 'data' in service_dict.keys():
                        fuel_type = service_dict['data']['fuel_type']
                        body_type = service_dict['data']['body_type']
                        if fuel_type != '':
                            getServiceList =  "https://droom.in/getRepairServicesList?trim_id="+trim_id+"&body_type="+body_type+"&fuel_type="+fuel_type
                            model_call = requests.get(getServiceList, headers = headers)
                            result = model_call.content
                            # print(result)
                            result_dict = json.loads(result.decode('utf-8'))
                            if result_dict['data'] != '':
                                prices_soup = BeautifulSoup(result, 'lxml')
                                body_soup = prices_soup.find_all('div', attrs = {'id':'\\"outer-body-repair-service\\"'})
                                parts = body_soup[0].find_all('input')
                                prices_list = []
                                for part, part_name in zip(parts, names_list):
                                    prices_dict = {}
                                    # part_name = part.attrs['value'].strip('\\"')
                                    prices_dict['part_name'] = part_name
                                    price_min = part.attrs['data-price-min'].strip('\\"')
                                    prices_dict['price_min'] = price_min
                                    price_max = part.attrs['data-price-max'].strip('\\"')
                                    prices_dict['price_max'] = price_max
                                    prices_list.append(prices_dict)
                                service_dict['prices_list'] = prices_list
                                # print(prices_list)
                                trim_dict['data'] = service_dict
        model_dict['trim_list'] = trim_list
    make_dict['model_list'] = model_list