###Data###
#lists of normal and high demands for day t
D = [15,14,7,10,10,13,6,15,8,10,9,14,7,9]
H = [20,18,12,17,19,16,13,24,16,17,18,21,12,18]

#list of required 90kg cylinder demands
R = [2,3,4,5,5,5,5,4,5,3,3,4,5,4]

#selling prices
r,r2 = 120,230
#Storage capacities
M, M2 = 30, 2

#cost of deliverly
def cost(x1,x2):      
    if (x1 > 0) or (x2 > 0): 
        return 300 + 50 * x1 + 80*x2
    else:
        return 0

#memoisation
ppg_ = {}

###Value Function###
def ppg(t,s1,s2):
    if t > 13: #end case
        return (0,'done','done','done','done')
    elif (t,s1,s2) not in ppg_: #recursive case  
        #list of possible combinations to sell 90kg cylinders split into 2 45kg or 1 90kg
        #amounts = [(0,R[t])]
        amounts = [((R[t]-i)*2,i) for i in range(0,R[t]+1)]

        #value function
        ppg_[t,s1,s2] = max((0.6*r*min(D[t],s1+a-c45) + 0.4*r*min(H[t],s1+a-c45) + r2*(c45/2)+r2*(c90)  - cost(a,a2) \
                            + 0.6*ppg(t+1, min(M, s1 + a - min(D[t],s1+a-c45) - c45) , s2 + a2 - c90)[0] \
                            + 0.4*ppg(t+1, min(M, s1 + a - min(H[t],s1+a-c45) - c45) , s2 + a2 - c90)[0],a,a2,c45,c90) \
                            for (c45,c90) in amounts \
                            for a2 in range(max(0,c90 - s2), M2 + c90 - s2 + 1) \
                            for a in range(0,min(22, M + D[t]+ c45 - s1) + 1 ) if a*45 +a2*90 <= 1000)
    return ppg_[t,s1,s2]


print(ppg(0,0,0))
