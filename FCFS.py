import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Hàm tính toán FCFS
def fcfs(processes):
    n = len(processes)
    processes.sort(key=lambda x: x['Arrival time'])
    
    # Khởi tạo các giá trị tính toán
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    current_time = 0
    
    for i, process in enumerate(processes):
        service_time = process['Service time']
        arrival_time = process['Arrival time']
        
        # Thời gian bắt đầu xử lý
        start_time = max(current_time, arrival_time)
        
        # Thời gian đáp ứng (response time)
        response_time = start_time - arrival_time
        total_response_time += response_time
        process['Thời gian đáp ứng'] = response_time
        
        # Thời gian kết thúc (completion time)
        completion_time = start_time + service_time
        
        # Thời gian hoàn thành
        process['Thời gian hoàn thành'] = completion_time - arrival_time
        
        # Thời gian chờ nhận CPU (waiting time)
        waiting_time = completion_time - arrival_time - service_time
        total_waiting_time += waiting_time
        process['Thời gian chờ nhận CPU'] = waiting_time
        
        # Thời gian xử lý (turnaround time)
        turnaround_time = completion_time - arrival_time
        total_turnaround_time += turnaround_time
        
        current_time = completion_time
    
    avg_response_time = total_response_time / n
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    
    return processes, avg_response_time, avg_waiting_time, avg_turnaround_time

# Hàm vẽ biểu đồ Gantt
def plot_gantt(processes):
    fig, ax = plt.subplots()
    y_labels = []
    start_times = []
    end_times = []

    for process in processes:
        y_labels.append(process['Process name'])
        start_times.append(max(process['Arrival time'], end_times[-1] if end_times else 0))
        end_time = start_times[-1] + process['Service time']
        end_times.append(end_time)

    ax.barh(y_labels, [end - start for start, end in zip(start_times, end_times)],
             left=start_times, color='skyblue')

    ax.set_xlabel('Time')
    ax.set_title('Gantt Chart for FCFS Scheduling')
    plt.grid(axis='x')
    st.pyplot(fig)

# Giao diện Streamlit
st.title('FCFS CPU Scheduling Algorithm')

# Tạo form nhập dữ liệu cho các tiến trình
processes = []
num_processes = st.number_input('Số lượng tiến trình:', min_value=1, value=1)

for i in range(num_processes):
    process_name = f'P{i+1}'  # Tự động đặt tên tiến trình là P1, P2, P3...
    service_time = st.number_input(f'Thời gian sử dụng CPU (service time) của {process_name}:', min_value=1)
    arrival_time = st.number_input(f'Thời gian đến (arrival time) của {process_name}:', min_value=0)
    
    processes.append({
        'Process name': process_name,
        'Service time': service_time,
        'Arrival time': arrival_time
    })

# Nút tính toán
if st.button('Tính toán FCFS'):
    # Thực hiện tính toán
    processes, avg_response_time, avg_waiting_time, avg_turnaround_time = fcfs(processes)
    
    # Hiển thị kết quả
    df = pd.DataFrame(processes)
    st.write(df)
    
    st.write(f'Thời gian đáp ứng trung bình: {avg_response_time:.2f}')
    st.write(f'Thời gian chờ nhận CPU trung bình: {avg_waiting_time:.2f}')
    st.write(f'Thời gian hoàn thành trung bình: {avg_turnaround_time:.2f}')
    
    # Vẽ biểu đồ Gantt
    plot_gantt(processes)  # Gọi hàm vẽ biểu đồ Gantt
