R1,R2=map(int,input().split());
S1=3.14*R1*R1;
S2=3.14*R2*R2;
S3=3.14*(R1*R1-R2*R2);
print(f"{S1:.2f}",f"{S2:.2f}",f"{S3:.2f}")