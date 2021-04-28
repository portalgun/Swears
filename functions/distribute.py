def distribute(A,B):
    A=np.array(A)
    B=np.array(B)
    C=np.repeat(A,B.size)
    C=np.array(C,ndmin=2)
    D=ml.repmat(B,1,A.size)
    F=np.concatenate((C,D),axis=0)
    return F
