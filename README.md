# python-zabbix
## Synopsis
        1         2         3         4         5         6         7        8
123456780123456789012345678901234567890123456789012345678901234567890123456890     
This package implements vartious pure Python tools for Zabbix monitor
development. This package provides the following;
  1.  Zabbix sender: 
  2.  Zabbix get:
  3.  Zabbix active check: 

## Motivation
I was not happy with any of the existing pure Python senders for Zabbix, so I
decided to write my own. And then I decided to add other features...

## Code Examples
###     Send a single item to the Zabbix server;
```python
      from zabbix import Sender
      zabbix = Sender(zabbix_serv='localhost',zabbix_port=10051)
      zabbix.add_item(key='myKey1',value='16535')
      zabbix.send()
```

###     Send multiple items to the Zabbix server;
```python
      from zabbix import Sender
      zabbix = Sender()
      zabbix.add_item(key='myKey1',value='16535')
      zabbix.add_item(key='myKey2',value='16534')
      zabbix.add_item(key='myKey3',value='16533')
      zabbix.send()
```

###     Build zabbix data with multiple items, but display it instead of sending;
```python
      from zabbix import Sender
      zabbix = Sender()
      zabbix.add_item(key='myKey1',value='16535')
      zabbix.add_item(key='myKey2',value='16534')
      zabbix.add_item(key='myKey3',value='16533')
      zabbix.send(print_values=True)
```

###     Send multiple items to Zabbix iteratively;
```python
      from zabbix import Sender
      zabbix = Sender()
      zabbix.add_item(key='myKey1',value='16535')
      zabbix.add_item(key='myKey2',value='16534')
      zabbix.add_item(key='myKey3',value='16533')
      zabbix.send(iterate_values=True)
```

## Installation
### From GitHub
  git clone http://www.github.com/nikatjef/python-zabbix.git
  cd python-zabbix
  python setup.py install

  * You can also create your own apt or rpm package wth the following;
    - apt
      python setup.py --command-packages=stdeb.command bdist_deb

    - rpm
      python setup.py --command-packages=stdeb.command bdist_rpm

    - tar.gz
      python setup.py sdist

    - pypi package
      python setup.py bdist_wheel

### From pypy
  pip install python-zabbix

### From apt repository
  apt-get install python-zabbix

### From RPM repository
  yum install python-zabbix

## API Reference

## Tests

## Contributors

## License

## TODO

