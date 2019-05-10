import heapq


vals = [1,2,3,4,5,6,7,8,9]
k = 3

result = []
heapq.heapify(result)
for i in range(0, len(vals)):
    current_element = (vals[i] * -1)
    if len(result) < k:
        result.append(current_element)
    else:
        max = heapq.heappop(result)
        if max < current_element:
            heapq.heappush(result, current_element)
        else:
            heapq.heappush(result, max)

print result