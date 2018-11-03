import sys

def dispatch(flag,prob):
    import random
    import datetime
    msg = open('f_send.txt','r').read()
    p_factor = prob/len(msg)
    output_code = ""
    error_states = ""
    while len(msg) > 0:            
        if msg.find(flag) == 0:
            output_code+=msg[:len(flag)]
            msg = msg[len(flag):]
            error_states+=str("0"*len(flag))
        else:
            probability = len(output_code)*p_factor
            if probability == 0:
                output_code+=msg[0]
                error_states+="0"
            elif random.randint(1,int(1/probability)) == 1:
                error_states+="1"
                if msg[0] == "0":
                    output_code+="1"
                else:
                    output_code+="0"           
            else:
                output_code+=msg[0]
                error_states+="0"
            msg = msg[1:]
    noisy_msg = [output_code,error_states,str(datetime.datetime.now()),str(prob)]
    return(write_transmission(noisy_msg))

    
def write_transmission(data):
    wfile = open('medium_data_1.bin',"w")
    wfile.write("###".join(data))
    wfile.close()
    
    wfile = open('f_err.txt',"w")
    wfile.write(data[0])
    wfile.close()
    print("Message dispatched at:", data[2])
    
def evaluate():
    data = open('medium_data_1.bin','r').read()
    in_data = data.split("###")
    print("Evaluating 'f_detect.txt' with message dispatched on :",in_data[-1])
    out_data = []
    with open("f_detect.txt","r") as file:
        eo = 0
        for line in file:
            if eo == 0:
                frame = line.strip()
                eo = 1
            else:
                err = line.strip()
                out_data.append((frame,err))
                eo = 0
    p_factor = float(in_data[3])/len(in_data[0])
    ret_data = out_data
    disp_data = in_data[0]
    err_data = in_data[1]
    count = 0
    err_count = 0
    dtct_count = 0
    dt_err = [[0,0]]
    t_err = [[0,0]]
    while len(ret_data) > 0:
        frame_length = len(ret_data[0][0])
        count+=frame_length
        if disp_data[:frame_length] == ret_data[0][0]:
            if "1" in err_data[:frame_length]:
                err_count+=1
                t_err.append([count*p_factor,err_count])
                if ret_data[0][1] == "1":
                    dtct_count+=1
                    dt_err.append([count*p_factor,dtct_count])
            else:
                if ret_data[0][1] == "1":
                    print("No error but detected: ", ret_data[0])
            ret_data = ret_data[1:]
            disp_data = disp_data[frame_length:]
            err_data = err_data[frame_length:]
            
    x, y = zip(*dt_err)
    x2, y2 = zip(*t_err)

    import matplotlib.pyplot as plt
    l1, = plt.plot(x,y, label = "Detected Frames with Error(s)")
    first_legend = plt.legend(handles=[l1], loc=4)
    ax = plt.gca().add_artist(first_legend)
    l2, = plt.plot(x2,y2, label = "Total Frames with Error(s)",linestyle='--')
    plt.legend(handles=[l2], loc=2)
    plt.xlabel('Probability for Error')
    plt.ylabel('No. of Error-Frames')
    plt.show()
        
        
if __name__ == "__main__":
    a = (sys.argv[1])
    if a == "eval":
        evaluate()
    else:
        b = float(sys.argv[2])
        dispatch(a,b)
