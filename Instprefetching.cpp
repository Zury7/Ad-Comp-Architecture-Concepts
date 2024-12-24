int sum = 0;
#define N 100  
int a[N];  
int b[N];

for(i = 0; i < N; i++) { 
    fetch (&a[i+1]); 
    fetch (&b[i+1]); 
    
    sum += a[i]*b[i]; 
    }

fetch (&sum); 
fetch (&a[0]); 
fetch (&b[0]); 

for (i = 0; i < N-4; i+=4) { 
    fetch (&a[i+4]); 
    fetch (&b[i+4]); 
    sum += a[i]*b[i]; 
    sum += a[i+1]*b[i+1]; 
    sum += a[i+2]*b[i+2]; 
    sum += a[i+3]*b[i+3]; } 

for (i = N-4; i < N; i++) {
    sum = sum + a[i]*b[i];}

fetch (&sum); 
for (i = 0; i < 12; i += 4){ 
    fetch (&a[i]); 
    fetch (&b[i]); } 
for (i = 0; i < N-12; i += 4){ 
    fetch(&a[i+12]); 
    fetch(&b[i+12]); 
    sum = sum + a[i] *b[i]; 
    sum = sum + a[i+1]*b[i+1]; 
    sum = sum + a[i+2]*b[i+2]; 
    sum = sum + a[i+3]*b[i+3]; } 
for (i = N-12; i < N; i++) {
    sum = sum + a[i]*b[i]; }