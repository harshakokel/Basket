v=["Tm_1","Tm_2","Tm_3","Tn_1","Tn_2","Tn_3","To_1","To_2","To_3","Tmn_12","Tmn_13","Tmo_12","Tmo_13","Tmn_21","Tmn_23","Tmo_21","Tmo_23","Tmn_31","Tmn_32","Tmo_31","Tmo_32","Tno_12","Tno_13","Tno_21","Tno_23","Tno_31","Tno_32"];
f = zeros(1,27);
f(1) = -1;f(2) = -2;f(3) = -3;f(4) = -1;f(5) = -2;f(6) = -3;f(4) = -1;f(7) = -1;f(8) = -2;f(9) = -3;
T_m = zeros(1,27);
T_m(1) = 1; T_m(2) = 1; T_m(3) = 1;
T_n = zeros(1,27);
T_n(4) = 1; T_n(5) = 1; T_n(6) = 1;
T_o = zeros(1,27);
T_o(7) = 1; T_o(8) = 1; T_o(9) = 1;
T_mn_m_1 = zeros(1,27);
T_mn_m_1(find(v=="Tmn_12")) = 1;T_mn_m_1(find(v=="Tmn_13")) = 1;T_mn_m_1(find(v=="Tm_1")) = -1;
T_mo_m_1 = zeros(1,27);
T_mo_m_1(find(v=="Tmo_12")) = 1;T_mo_m_1(find(v=="Tmo_13")) = 1;T_mo_m_1(find(v=="Tm_1")) = -1;
T_mn_m_2 = zeros(1,27);
T_mn_m_2(find(v=="Tmn_21")) = 1;T_mn_m_2(find(v=="Tmn_23")) = 1;T_mn_m_2(find(v=="Tm_2")) = -1;
T_mo_m_2 = zeros(1,27);
T_mo_m_2(find(v=="Tmo_21")) = 1;T_mo_m_2(find(v=="Tmo_23")) = 1;T_mo_m_2(find(v=="Tm_2")) = -1;
T_mo_m_3 = zeros(1,27);
T_mo_m_3(find(v=="Tmo_31")) = 1;T_mo_m_3(find(v=="Tmo_32")) = 1;T_mo_m_3(find(v=="Tm_3")) = -1;
T_mn_m_3 = zeros(1,27);
T_mn_m_3(find(v=="Tmn_31")) = 1;T_mn_m_3(find(v=="Tmn_32")) = 1;T_mn_m_3(find(v=="Tm_3")) = -1;
T_mn_n_3 = zeros(1,27);
T_mn_n_3(find(v=="Tmn_13")) = 1;T_mn_n_3(find(v=="Tmn_23")) = 1;T_mn_n_3(find(v=="Tn_3")) = -1;
T_mn_n_2 = zeros(1,27);
T_mn_n_2(find(v=="Tmn_12")) = 1;T_mn_n_2(find(v=="Tmn_32")) = 1;T_mn_n_2(find(v=="Tn_2")) = -1;
T_mn_n_1 = zeros(1,27);
T_mn_n_1(find(v=="Tmn_21")) = 1;T_mn_n_1(find(v=="Tmn_31")) = 1;T_mn_n_1(find(v=="Tn_1")) = -1;
T_no_n_3 = zeros(1,27);
T_no_n_3(find(v=="Tno_31")) = 1;T_no_n_3(find(v=="Tno_32")) = 1;T_no_n_3(find(v=="Tn_3")) = -1;
T_no_n_1 = zeros(1,27);
T_no_n_1(find(v=="Tno_12")) = 1;T_no_n_1(find(v=="Tno_13")) = 1;T_no_n_1(find(v=="Tn_1")) = -1;
T_no_n_2 = zeros(1,27);
T_no_n_2(find(v=="Tno_21")) = 1;T_no_n_2(find(v=="Tno_23")) = 1;T_no_n_2(find(v=="Tn_2")) = -1;
T_mo_o_3 = zeros(1,27);
T_mo_o_3(find(v=="Tmo_13")) = 1;T_mo_o_3(find(v=="Tmo_23")) = 1;T_mo_o_3(find(v=="To_3")) = -1;
T_mo_o_2 = zeros(1,27);
T_mo_o_2(find(v=="Tmo_12")) = 1;T_mo_o_2(find(v=="Tmo_32")) = 1;T_mo_o_2(find(v=="To_2")) = -1;
T_mo_o_1 = zeros(1,27);
T_mo_o_1(find(v=="Tmo_21")) = 1;T_mo_o_1(find(v=="Tmo_31")) = 1;T_mo_o_1(find(v=="To_1")) = -1;
T_no_o_1 = zeros(1,27);
T_no_o_1(find(v=="Tno_21")) = 1;T_no_o_1(find(v=="Tno_31")) = 1;T_no_o_1(find(v=="To_1")) = -1;
T_no_o_2 = zeros(1,27);
T_no_o_2(find(v=="Tno_12")) = 1;T_no_o_2(find(v=="Tno_32")) = 1;T_no_o_2(find(v=="To_2")) = -1;
T_no_o_3 = zeros(1,27);
T_no_o_3(find(v=="Tno_13")) = 1;T_no_o_3(find(v=="Tno_23")) = 1;T_no_o_3(find(v=="To_3")) = -1;
Aeq = [T_m;T_n;T_o;T_mn_m_2; T_mn_n_1 ; T_mn_n_3 ; T_mo_m_2 ; T_mo_o_1  ;T_mo_o_3 ; T_no_n_1;  T_no_n_3;  T_no_o_2;T_mn_m_1  ;T_mn_m_3  ;T_mn_n_2 ; T_mo_m_1 ; T_mo_m_3 ; T_mo_o_2 ; T_no_n_2 ; T_no_o_1;T_no_o_3]
beq = zeros(21,1)
beq(1) = 1;beq(2) = 1;beq(3) = 1
lp = linprog(f,[],[],Aeq,beq,zeros(size(f)),ones(size(f)))
[v',lp]

ans = 

  27×2 string array

    "Tm_1"      "0"  
    "Tm_2"      "0.5"
    "Tm_3"      "0.5"
    "Tn_1"      "0"  
    "Tn_2"      "0.5"
    "Tn_3"      "0.5"
    "To_1"      "0"  
    "To_2"      "0.5"
    "To_3"      "0.5"
    "Tmn_12"    "0"  
    "Tmn_13"    "0"  
    "Tmo_12"    "0"  
    "Tmo_13"    "0"  
    "Tmn_21"    "0"  
    "Tmn_23"    "0.5"
    "Tmo_21"    "0"  
    "Tmo_23"    "0.5"
    "Tmn_31"    "0"  
    "Tmn_32"    "0.5"
    "Tmo_31"    "0"  
    "Tmo_32"    "0.5"
    "Tno_12"    "0"  
    "Tno_13"    "0"  
    "Tno_21"    "0"  
    "Tno_23"    "0.5"
    "Tno_31"    "0"  
    "Tno_32"    "0.5"

f*lp

ans =

   -7.5000

