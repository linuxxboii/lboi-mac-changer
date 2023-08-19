import subprocess # Dış sistem komutlarını çalıştırmak için kullanılan bir modül.
import optparse # Komut satırı argümanlarını işlemek için kullanılan bir modül.
import re # Düzenli ifadeleri işlemek için kullanılan bir modül.

# Kullanıcıdan ağ arayüzünün adını ve yeni MAC adresini almak için bir işlev.
def info_gather():
    parser = optparse.OptionParser() # Komut satırı argümanlarını işlemek için bir nesne oluştur.
    
    # -i veya --interface ile kullanıcıdan ağ arayüzünün adını al.
    parser.add_option("-i","--interface", dest= "user_interface", help="degistirmek istediginiz arayuzu seciniz")
    # -m veya --mac ile kullanıcıdan yeni MAC adresini al.
    parser.add_option("-m","--mac", dest="user_mac_adresi", help="yeni mac adresini giriniz...")

    return parser.parse_args() # Kullanıcının girdilerini al ve işle.

# Belirtilen ağ arayüzünü kapat, yeni MAC adresini ayarla ve tekrar açan bir işlev.
def terminal(user_interface, user_mac_adresi):
    subprocess.call(["ifconfig", user_interface, "down"]) # Belirtilen arayüzü kapat.
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_adresi]) # Yeni MAC adresini ayarla.
    subprocess.call(["ifconfig", user_interface, "up"]) # Arayüzü tekrar aç.

# Yeni MAC adresinin belirtilen arayüzde başarıyla değiştirilip değiştirilmediğini kontrol eden bir işlev.
def controlling_new_mac(user_interface):
    subprocess.call(["ifconfig", user_interface]) # Arayüzün bilgilerini görüntüle.
    
    # Düzenli ifade kullanarak yeni MAC adresini bulmaya çalış.
    yeni_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", "ifconfig")

    if yeni_mac:
        return yeni_mac.group(0) # Bulunan yeni MAC adresini döndür.
    else:
        return None # Yeni MAC adresi bulunamazsa hiçbir şey döndürme.

print("mac degistirici basladi...")

# Kullanıcıdan girdileri al.
(user_input, arguments) = info_gather()

# Belirtilen arayüzdeki MAC adresini değiştir.
terminal(user_input.user_interface, user_input.user_mac_adresi)

# Yeni MAC adresini kontrol et.
bitmis_mac = controlling_new_mac(user_input.user_interface)

# Eğer yeni MAC adresi beklenenle aynı değilse, değiştirme işleminin başarılı olduğunu bildir.
if bitmis_mac != user_input.user_mac_adresi:
    print("mac degistirme islemi basarili")
else:
    print("mac degistirme islemi basarisiz...")
