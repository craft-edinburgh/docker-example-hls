// This is the function to be synthesized into hardware/Verilog
int top(int a[10]) {
  int accum = 0;
  for (int i = 0; i < 10; i++)
    accum += a[i];
  return accum;
}

// This is the C function used to test the top function at the C level, also
// known as its test bench
int main() {
  int b[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  int k = top(b);
  return 0;
}
