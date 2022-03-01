read_input();
while(swirl_counter < mem[31]){ // 32 loops
    swirl();
    add_or_smth();
    swirl_counter++;
}

for(int iter = 0; i < flag_len; ++i){
    if(enc_flag[iter] != input_flag[iter]){
        stdout_string("Wrong!\n"); // "Wrong!"
        exit();
    }
}

stdout_string("Correct!"); // "Correct!"
exit();


void read_input(){
    for(int g_iter = 0; g_iter < g_flag_len; ++i){
        stdout_string("flag["); // "flag[" 
        stdout_number(g_iter);  // counter (mem[28])
        stdout_string("]: ");   // "]:"

        do{
            temp = input(); // input
        }while(temp < 1);

        g_input_flag[g_iter] = temp;

        stdout_char(temp);
        stdout_char("\n"); // "\n"
    }
    return;
}

void swirl(){
    for(int iter = 0; i < g_input_flag_len; ++i){
        temp = g_input_flag[iter];
        g_input_flag[iter] = g_input_flag[swirl[iter]];
        g_input_flag[swirl[iter]] = temp;
    }
    return;
}

void mess(){
    for(int iter = 0; i < flag_len; ++i){
        g_input_flag[iter] = mapper[(iter + swirl_counter + 11) % flag_len]
    }
    return;
}
