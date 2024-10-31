import streamlit as st
import pandas as pd
from io import StringIO
from generator import file_genrator
import subprocess
import time
import re







def main():
    # query()
    # print(query())
    st.write("Extended SQL Query Processor")

select_arg_array = []



with st.form("phi-oprtator"):
   st.write("Enter 6 arguements for phi operators")
   select_arg = st.text_input("S: List of projected attributes for the query output", key="select_arg")
   n_arg = st.number_input("n: Number of grouping variables", key="n_arg",value=0, min_value=0, step=1)
   v_arg = st.text_input("v: List of grouping attributes", key="v_arg")
   f_arg = st.text_input("f:  list of sets of aggregate functions. Fi represents a list of aggregate functions for each grouping variable", key="f_arg")
   predicates_arg = st.text_input("P: list of predicates to define the ranges for the grouping variables", key="predicates_arg")
   having_arg = st.text_input("G: Predicate for the having clause(Optional)", key="having_arg")
   f_arg_list = []
#    print(select_arg)
   submitted = st.form_submit_button("Submit")
   if submitted:
    if not select_arg or not n_arg or not v_arg or not f_arg :
        st.error('Please input all the fields.')  
    else:
        select_arg_list = [x.strip() for x in select_arg.split(',')] 
        v_grp_attr_list = [x.strip() for x in v_arg.split(',')]
    #    if set(select_arg_list) != set(v_grp_attr_list):
    #         st.error('Attributes in "S" must be the same as attributes in "V"')
    #    else:     
        f_arg_list = [x.strip() for x in f_arg.split(',')]
        print(f_arg_list)
        f = [[] for _ in range(len(f_arg.split(',')[-1].split('_')[0])+1)]
        f.append([])
        print(f)
        for item in f_arg_list:
            index = int(item.split('_')[0])
            print(item,index)
            f[index].append(item)

        predi_arg_list = [x.strip() for x in predicates_arg.split(',')]
        values = []
        values.append([])
        for item in predi_arg_list:
         value = re.sub(r'\d+\.', '', item)
         values.append([value])  

        having_list = [x.strip() for x in having_arg.split(',')]

    print(f'select is {select_arg_list}, n is {n_arg}, v is {v_grp_attr_list}, f is {f}, predicates are {values} ,having is {having_list}')
    file_genrator(s=select_arg_list,n=n_arg,v_list=v_grp_attr_list,f_list = f,pred_list = values,having_list = having_list)
    # time.sleep(10)
    
    from _generated import query
    rd = query()
    # print(rd)
    st.dataframe(rd[0])
    st.write('Completed')
    print("Heyyyy ",type(rd))




uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.type != 'text/plain':
        st.error('Please upload a text file')
    else:    

    # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
        string_data = bytes_data.decode("utf-8")
        lines = string_data.split('\n')

        first_line = lines[0].strip()
        select_arg_list = [x.strip() for x in first_line.split(',')]

        second_line = lines[1].strip()
        try:
         n_arg = int(second_line)
        except:
         st.error('Second line should be an integer.')   

        third_line = lines[2].strip()
        v_grp_attr_list = [x.strip() for x in third_line.split(',')]

        fourth_line = lines[3].strip()
        f_arg_list = [x.strip() for x in fourth_line.split(',')]
        print(f_arg_list)
        f = [[] for _ in range(len(fourth_line.split(',')[-1].split('_')[0])+1)]
        f.append([])
        print(f)
        for item in f_arg_list:
            index = int(item.split('_')[0])
            print(item,index)
            f[index].append(item)
         


    

        fifth_line = lines[4].strip()
        predi_arg_list = [x.strip() for x in fifth_line.split(',')] 
        values = []
        values.append([])
        for item in predi_arg_list:
         value = re.sub(r'\d+\.', '', item)
         values.append([value])  
  

        sixth_line = lines[5].strip()
        if sixth_line:
            having_list = [x.strip() for x in sixth_line.split(',')]
        else:
            having_list = []

        print(f'select is {select_arg_list}, n is {n_arg}, v is {v_grp_attr_list}, f is {f}, predicates are {values} ,having is {having_list}')
        file_genrator(s=select_arg_list,n=n_arg,v_list=v_grp_attr_list,f_list = f,pred_list = values,having_list = having_list)
        time.sleep(1)
        
        from _generated import query
        
        output = query()
    # print(rd)
        st.dataframe(output[0])
        st.write(f'Number of Scans {output[1]} ')
    
    
if "__main__" == __name__:
    main()