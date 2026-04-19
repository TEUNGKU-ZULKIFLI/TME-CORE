# Physical Router Setup (RB750Gr2) - Step by Step

## A. Prioritas Keamanan Awal (WAJIB)
Kondisi saat ini: akun admin tanpa password.

1) Set password admin segera.
2) Jika memungkinkan, buat user admin baru lalu nonaktifkan default admin.
3) Batasi akses manajemen dari subnet lab saja.

Contoh perintah RouterOS (jalankan di terminal MikroTik):
```rsc
/user set [find name=admin] password=<PASSWORD_BARU_KUAT>
/ip service disable telnet
/ip service disable ftp
/ip service disable www
/ip service disable www-ssl
/ip service disable api-ssl
/ip service set api disabled=no port=8728
```

Catatan: jika ingin keamanan lebih tinggi gunakan api-ssl dengan sertifikat, tapi untuk fase awal lab boleh mulai dari api lalu dibatasi via firewall.

## B. Batasi Akses API ke Controller Saja
Ganti <IP_DEBIAN_WSL> dengan IP engine controller.

```rsc
/ip firewall filter add chain=input action=accept src-address=<IP_DEBIAN_WSL> protocol=tcp dst-port=8728 comment="Allow API from controller"
/ip firewall filter add chain=input action=drop protocol=tcp dst-port=8728 comment="Drop other API access"
```

## C. Verifikasi dari Sisi Router
```rsc
/ip service print
/ip firewall filter print where dst-port=8728
/system resource print
```

## D. Verifikasi dari Debian WSL
1) Cek reachability:
```bash
ping -c 4 <IP_ROUTER>
```
2) Cek port API:
```bash
nc -zv <IP_ROUTER> 8728
```
3) Jika gagal, cek WSL2 networking (route/firewall Windows).

## E. Checklist Selesai
- [ ] Password admin terpasang
- [ ] API port aktif
- [ ] API hanya bisa diakses controller
- [ ] Reachability dari Debian OK
- [ ] Logging eksperimen siap dijalankan
