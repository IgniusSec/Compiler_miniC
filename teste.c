int main() {

  int x;
  x = 10;
  float y;
  y = 3.14;
  char c_a;
  c_a = 'A';
  char s[8];
  s = "hello";

  if (x >= 10 && y < 4.0) {
    x = x + 1;
  } else {
    x = x - 1;
  }

  while (x != 0) {
    x = x - 1;
    continue;
    break;
  }

  for (int i = 0; i < 10; i = i + 1) {
    x = x + i;
  }

  float array[1];
  array[0] = x * 2 % 5 / y;
}
