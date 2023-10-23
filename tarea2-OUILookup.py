import subprocess
import platform
import ipaddress
import subprocess
import getopt
import sys

# Base de datos de fabricantes de tarjetas de red

# DATOS DE EJEMPLOOOOOOOOO EN EL ARCHIVO DE PRUEBA QUE SE NOS ASIGNÓ||||
#                                                                   VVVV

def cargar_base_de_datos():
    base_de_datos = {}
    try:
        with open("BaseDatosMac.txt", "r") as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    mac = parts[0].strip()
                    vendor = parts[1].strip()
                    base_de_datos[mac] = vendor
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'BaseDatosMac.txt'")
    return base_de_datos

base_de_datos = cargar_base_de_datos()

  #MAC asociada al fabricante:Nombre del fabricante





# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    print("\n Direccion IP:", ip)
    if es_misma_red(ip, "192.168.1.30", "255.255.255.0"):
        mac = obtener_mac_por_ip(ip)
        if mac:
            fabricante = buscar_fabricante(mac)
            if fabricante:
                print("Direccion Mac:", mac)
                print("Fabricante:", fabricante+"\n")
            else:
                print("Fabricante: No encontrado"+"\n")

        else:
            print("Error: No se pudo obtener la MAC para la IP proporcionada."+"\n")
    else:
        print("Error: La IP está fuera de la red del host.")





# Función para determinar si una IP está en la misma red, usando la ip y una mascara
def es_misma_red(ip, host_ip, mascara):
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        host_ip_obj = ipaddress.IPv4Network(f"{host_ip}/{mascara}", strict=False)
        return ip_obj in host_ip_obj
    except ipaddress.AddressValueError:
        return False


# Función para obtener la MAC por IP 
def obtener_mac_por_ip(ip):
    if es_misma_red(ip, "192.168.1.30", "255.255.255.0"):
        # Simulamos la obtención de la MAC por IP aquí.
        # Devuelve la MAC si es posible, None en caso contrario.
        mac = "b4:b5:fe:92:ff:c5"  # Ejemplo de MAC simulada
        return mac
    else:
        return None


# Función para buscar el fabricante en la base de datos de MAC
def buscar_fabricante(mac):
    return base_de_datos.get(mac[:8], "Not found")




# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    fabricante = buscar_fabricante(mac)
    print("\nMAC address:", mac)
    if fabricante:
        print("Fabricante:", fabricante+"\n")
    else:
        print("Fabricante: No encontrado \n")

# Función para obtener la tabla ARP           #COMENTARIO IMPORTANTE: EL CODIGO ME FUNCIONABA BIEN EN OTRO ENTORNO PERO AL CAMBIAR DE ENTERNO LA FUNCION OBTENER_TABLA_ARP DA ERROR PORQUE EL COMANDO ARP Y -A PARECE QUE TIENE INCOMPATIBILIDAD CON WINDOWS Y SOLO ME FUNCIONÓ EN LINUX 
def obtener_tabla_arp():
            sistema_operativo = platform.system()  # Obtiene el nombre del sistema operativo
            if sistema_operativo == "Windows":
                try:
                    arp_result = subprocess.check_output(["arp", "-a"], universal_newlines=True)
                    print("IP/MAC/Vendor:")
                    for line in arp_result.splitlines():
                        if "Internet Address" in line:
                            parts = line.split()
                            ip = parts[1]
                            mac = parts[3]
                            fabricante = buscar_fabricante(mac)
                            print(f"{ip} / {mac} / {fabricante}")
                except subprocess.CalledProcessError:
                    print("Error al obtener la tabla ARP en Windows.")
            elif sistema_operativo == "Linux" or sistema_operativo == "Darwin":  # Linux o macOS
                try:
                    arp_result = subprocess.check_output(["arp", "-n"], universal_newlines=True)
                    print("IP/MAC/Vendor:")
                    for line in arp_result.splitlines():
                        parts = line.split()
                        if len(parts) >= 3:
                            ip = parts[0]
                            mac = parts[2]
                            fabricante = buscar_fabricante(mac)
                            print(f"{ip} / {mac} / {fabricante}")
                except subprocess.CalledProcessError:
                    print("Error al obtener la tabla ARP en Linux o macOS.")
            else:
                print(f"Sistema operativo no compatible: {sistema_operativo}")

def main():
    while True:
        print("Ingrese una opcion (--ip , --mac o --arp) --help para ayuda")
        opcion = input("Opción: ")

        if opcion == "--ip":
            ip = input("Ingrese la dirección IP: ")
            obtener_datos_por_ip(ip)
        elif opcion == "--mac":
            mac = input("Ingrese la dirección MAC: ")
            obtener_datos_por_mac(mac)
        elif opcion == "--arp":
            obtener_tabla_arp()
        elif opcion == "--help":
            print("\n--ip : IP del host a consultar.\n--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n--arp: muestra los fabricantes de los host disponibles en la tabla arp.\n--help: muestra este mensaje y termina.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
