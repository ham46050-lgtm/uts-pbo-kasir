"""
Sistem Kasir Sederhana (OOP Python)
UTS Pemrograman Berorientasi Objek - 3C Ilmu Komputer

Konsep OOP yang diterapkan:
- Class & Object        : Produk, ProdukDiskon, Keranjang, Kasir
- Constructor __init__  : di semua class
- Attribute & Method    : data dan perilaku tiap class
- Encapsulation         : atribut private (diawali __)
- Property & Setter     : Produk.harga, Produk.stok, Kasir.nama
- Class method          : Produk.dari_string(), Kasir.total_transaksi()
- Static method         : Kasir.format_rupiah(), Kasir.hitung_kembalian()
- Inheritance/Override  : ProdukDiskon (bonus)
"""


class Produk:
    """Barang yang dijual di toko."""

    jumlah_produk = 0  # class attribute

    def __init__(self, kode, nama, harga, stok):
        self.__kode = kode
        self.nama = nama
        self.__harga = 0
        self.__stok = 0
        self.harga = harga      # lewat setter
        self.stok = stok        # lewat setter
        Produk.jumlah_produk += 1

    @property
    def kode(self):
        return self.__kode      # read-only

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        if nilai <= 0:
            raise ValueError("Harga harus lebih dari 0!")
        self.__harga = nilai

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self.__stok = nilai

    def harga_jual(self):
        return self.__harga

    def __str__(self):
        return f"[{self.__kode}] {self.nama} - {Kasir.format_rupiah(self.harga_jual())} (stok: {self.__stok})"

    @classmethod
    def dari_string(cls, teks):
        """Buat Produk dari string 'kode;nama;harga;stok'."""
        kode, nama, harga, stok = teks.split(";")
        return cls(kode, nama, int(harga), int(stok))


class ProdukDiskon(Produk):
    """Inheritance: produk dengan potongan harga (persen)."""

    def __init__(self, kode, nama, harga, stok, diskon_persen):
        super().__init__(kode, nama, harga, stok)
        self.__diskon = diskon_persen

    def harga_jual(self):       # method overriding
        return int(self.harga * (100 - self.__diskon) / 100)


class Keranjang:
    """Keranjang belanja satu transaksi."""

    def __init__(self):
        self.__item = []        # list of (produk, jumlah)

    def tambah(self, produk, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0!")
        if jumlah > produk.stok:
            raise Exception(f"Stok '{produk.nama}' tidak cukup (sisa {produk.stok}).")
        produk.stok -= jumlah
        self.__item.append((produk, jumlah))

    def total(self):
        return sum(p.harga_jual() * j for p, j in self.__item)

    @property
    def item(self):
        return list(self.__item)


class Kasir:
    """Kasir yang memproses transaksi."""

    __transaksi = 0  # private class attribute

    def __init__(self, nama):
        self.__nama = ""
        self.nama = nama
        self.__pendapatan = 0

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not nilai.strip():
            raise ValueError("Nama kasir tidak boleh kosong!")
        self.__nama = nilai.strip().title()

    @property
    def pendapatan(self):
        return self.__pendapatan

    def proses(self, keranjang, uang_bayar):
        total = keranjang.total()
        kembalian = self.hitung_kembalian(total, uang_bayar)
        self.__pendapatan += total
        Kasir.__transaksi += 1
        self.cetak_struk(keranjang, total, uang_bayar, kembalian)

    def cetak_struk(self, keranjang, total, bayar, kembalian):
        print(f"\n===== STRUK #{Kasir.__transaksi} | Kasir: {self.nama} =====")
        for p, j in keranjang.item:
            print(f"{p.nama:<18}{j:>3} x {self.format_rupiah(p.harga_jual()):>10} "
                  f"= {self.format_rupiah(p.harga_jual() * j):>11}")
        print("-" * 46)
        print(f"{'TOTAL':<28}{self.format_rupiah(total):>18}")
        print(f"{'BAYAR':<28}{self.format_rupiah(bayar):>18}")
        print(f"{'KEMBALI':<28}{self.format_rupiah(kembalian):>18}")

    @classmethod
    def total_transaksi(cls):
        return cls.__transaksi

    @staticmethod
    def format_rupiah(angka):
        return "Rp" + f"{angka:,}".replace(",", ".")

    @staticmethod
    def hitung_kembalian(total, bayar):
        if bayar < total:
            raise ValueError(f"Uang kurang {Kasir.format_rupiah(total - bayar)}!")
        return bayar - total


def main():
    beras = Produk("P01", "Beras 5kg", 65000, 10)
    minyak = Produk("P02", "Minyak Goreng 2L", 38000, 5)
    mie = ProdukDiskon("P03", "Mie Instan", 3500, 40, diskon_persen=10)
    kopi = Produk.dari_string("P04;Kopi Sachet;2000;100")

    print("=== Daftar Produk ===")
    for p in (beras, minyak, mie, kopi):
        print(" ", p)

    kasir = Kasir("budi santoso")

    # Transaksi 1: berhasil
    k1 = Keranjang()
    k1.tambah(beras, 1)
    k1.tambah(mie, 5)
    k1.tambah(kopi, 10)
    kasir.proses(k1, 150000)

    # Transaksi 2: gagal (stok / uang kurang / setter)
    for aksi in (
        lambda: Keranjang().tambah(minyak, 9),
        lambda: kasir.proses(_keranjang_minyak(minyak), 10000),
        lambda: setattr(beras, "harga", -100),
    ):
        try:
            aksi()
        except Exception as e:
            print(f"\nGAGAL: {e}")

    print(f"\nPendapatan kasir      : {Kasir.format_rupiah(kasir.pendapatan)}")
    print(f"Total transaksi       : {Kasir.total_transaksi()}")
    print(f"Jumlah produk dibuat  : {Produk.jumlah_produk}")


def _keranjang_minyak(minyak):
    k = Keranjang()
    k.tambah(minyak, 1)
    return k


if __name__ == "__main__":
    main()