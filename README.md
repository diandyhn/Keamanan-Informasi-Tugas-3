Nama Anggota:

Andi Aliyah Nur Inayah - 5025221196 <br>
Dian Kusumawati - 5025221106 <br>

<h1> Simple DES Encryption and Decryption </h1>
<h3>Deskripsi</h3>
<p> Program ini adalah implementasi sederhana dari Data Encryption Standard (DES), sebuah algoritma enkripsi simetris yang bekerja dengan kunci 10-bit dan memproses pesan biner 8-bit. Program ini melakukan enkripsi dan dekripsi melalui beberapa tahap, termasuk permutasi, substitusi, ekspansi, dan XOR.

Kelas DES mendefinisikan fungsi untuk proses enkripsi dan dekripsi menggunakan dua subkunci yang dihasilkan dari kunci utama 10-bit. S-Box dan permutasi yang diterapkan di dalam kelas ini disederhanakan dari standar DES yang sesungguhnya untuk keperluan pembelajaran. </p>

<h3>Struktur Program</h3>
    Program ini terbagi dalam beberapa fungsi utama:

- Initial Permutation (P8): Mengatur ulang bit pesan awal sebelum enkripsi.
- Key Scheduling: Menghasilkan dua subkunci k1 dan k2 dari kunci utama dengan permutasi dan pergeseran bit.
- S-Box Substitution: Menggunakan dua tabel S-Box (s0 dan s1) untuk melakukan substitusi non-linear, menambahkan kompleksitas pada enkripsi.
- Expansion-Permutation: Memperluas 4-bit menjadi 8-bit sebagai input untuk fungsi fFunction.
- fFunction: Fungsi inti yang mencakup ekspansi, substitusi, dan permutasi.
- Reverse Permutation (IP-1): Mengembalikan bit pada posisi semula setelah dua putaran enkripsi atau dekripsi selesai.
- Padding: Menambahkan padding 0 pada pesan untuk memenuhi panjang bit tertentu.

<h4>Fitur Utama</h4>

- Enkripsi: Menggunakan kunci utama untuk mengenkripsi pesan biner 8-bit menjadi pesan yang terenkripsi.
- Dekripsi: Mengembalikan pesan terenkripsi ke bentuk aslinya menggunakan proses yang mirip dengan enkripsi namun dengan urutan kunci yang terbalik.
- Kelas DES: Menyediakan antarmuka untuk memanggil metode Encryption dan Decryption dengan kunci yang sudah diatur dalam kelas ini.

<h3>Struktur Kelas dan Fungsi Utama</h3>

- Konstruktor (`__init__`): Menginisialisasi kunci utama dan mendefinisikan tabel S-Box.
- fFunction: Menggabungkan beberapa operasi untuk memproses setiap bagian pesan dalam enkripsi.
- kValueGenerator: Membuat dua subkunci (k1 dan k2) untuk digunakan dalam dua putaran enkripsi dan dekripsi.
- Encryption: Mengimplementasikan dua putaran enkripsi dengan k1 dan k2.
- Decryption: Melakukan proses dekripsi dengan urutan kunci terbalik untuk mengembalikan pesan asli.

<h3>Cara Penggunaan</h3>
Jalankan pada terminal

```
python3 server
```

dan

```
python3 client
```

<h3>Struktur Proses</h3>

- Permutasi Awal: Memulai dengan mengatur ulang bit dalam pesan.
- Putaran Pertama: Menggunakan fFunction dengan k1 dan melakukan XOR.
- Putaran Kedua: Menggunakan fFunction dengan k2 dan melakukan XOR.
- Permutasi Balik: Mengembalikan bit ke posisi semula untuk menghasilkan pesan akhir.