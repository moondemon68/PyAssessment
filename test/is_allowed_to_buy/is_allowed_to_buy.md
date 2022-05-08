# Is Allowed to Buy
## Soal
Diberikan empat buah integer soap, mask, sanitizer, dan face_shield yang masing-masing menyatakan jumlah sabun, masker, hand sanitizer dan face shield. Karena keterbatasan suplai, maka setiap pengunjung hanya boleh membeli barang tersebut secara terbatas. Berikut adalah syarat-syarat yang harus dipenuhi:
- Jumlah sabun yang dibeli harus tidak lebih besar dari 3.
- Jumlah hand sanitizer yang dibeli harus tidak lebih besar dari 3. Jika sudah membeli sabun, maka hand sanitizer yang dibeli harus tidak lebih besar dari 2.
- Jumlah masker yang dibeli harus tidak lebih besar dari 4. Jika sudah membeli face shield, maka masker yang dibeli harus tidak lebih besar dari 2.
- Jumlah face shield yang dibeli harus tidak lebih besar dari 4. Jika sudah membeli masker, maka face shield yang dibeli harus tidak lebih besar dari 2.
## Input
- soap: integer (-5 ≤ soap ≤ 10)
- masker: integer (-5 ≤ masker ≤ 10)
- sanitizer: integer (-5 ≤ sanitizer ≤ 10)
- face_shield: integer (-5 ≤ face_shield ≤ 10)
## Output
- Sebuah boolean yang menunjukkan apakah keranjang belanja pengunjung valid.
## Contoh Input 1
```
2, 3, 4, 5
```
## Contoh Output 1
```
false
```
## Contoh Input 2
```
1, 1, 1, 1
```
## Contoh Output 2
```
true
```