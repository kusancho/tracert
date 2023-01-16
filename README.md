# Traceroute

Course project within the course "Компьютерные сети"

## Requirements

- Python 3 or later

## Usage
```
sudo python3 main.py -d <destination> --hops <hops>
```

### Example

```
sudo python3 main.py -d ya.ru
```

### Output

```
traceroute to 87.250.250.242 (ya.ru), 30 hops max
1   router.asus.com (192.168.1.1) 4.0 ms 
2   100.122.0.1 (100.122.0.1) 6.0 ms 
3   * 
4   * 
5   belonogova.corbina.net (83.102.145.186) 19.0 ms 
6   sas-32z3-ae1.yndx.net (87.250.239.183) 126.0 ms 
7   * 
8   ya.ru (87.250.250.242) 18.0 ms 
