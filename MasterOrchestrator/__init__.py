import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    connection_string = "DefaultEndpointsProtocol=https;AccountName=mrstorageaccount1998;AccountKey=jTaKD0xbxiTpayzxYs3kqoMNHkaSOk9lNuIb9kdZk+ALxmjE5aW91yJtTb/+Gq+elyMqDgn7Ico++ASt6ynr8Q==;EndpointSuffix=core.windows.net"
    input_data = yield context.call_activity('GetDataFn', connection_string)

    # Fan-out: Call multiple instances of the 'Mapper' function in parallel
    map_tasks = []
    for data in input_data:
        map_tasks.append(context.call_activity('Mapper', data))
    map_results = yield context.task_all(map_tasks)

    # Flatten the list before sending it to shuffler
    map_results = sum(map_results, [])

    shuffle_result = yield context.call_activity('Shuffler', map_results)

    # Fan-out: Call multiple instances of the 'Reducer' function in parallel
    reduce_tasks = []
    for data in shuffle_result:
        reduce_tasks.append(context.call_activity('Reducer', (data, shuffle_result[data])))
    
    # Fan-in:
    reduce_results = yield context.task_all(reduce_tasks)

    return reduce_results

main = df.Orchestrator.create(orchestrator_function)
