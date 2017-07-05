# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *

Session = sessionmaker(bind=engine)

class PricesPipeline(object):

    # def open_spider(self, spider):
    #     # Open DB here
    #     Session = sessionmaker(bind=engine)
    #     self.session = Session()
    #     pass
    #
    # def close_spider(self, spider):
    #     # Close DB here
    #     pass

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        pass

    def process_item(self, item, spider):
        print('Product info of {} scrapped'.format(item['name']))

        self.session = Session()
        specs = '\n'.join([key + ":" + value for key, value in item['specs'].items()])
        if(self.session.query(Product).filter(Product.product_url==item['url']).count()):
            product = self.session.query(Product).filter(Product.product_url==item['url']).first()
            product.product_name = item['name']
            product.product_specs = specs
            product.product_url = item['url']
        else:
            product = Product(product_name=item['name'], product_specs=specs, product_url=item['url'])
        self.session.add(product)
        self.session.commit()

        for store_str, storeData in item['stores'].items():
            if self.session.query(Store.id).filter_by(name=store_str).scalar():
                store = self.session.query(Store).filter(Store.name==store_str).first()
            else:
                store = Store(name=store_str)
                self.session.add(store)
                self.session.commit()

            if self.session.query(ProductStore).filter(ProductStore.product_id==product.id,
                                                       ProductStore.store_id==store.id).count():
                productstore = self.session.query(ProductStore).filter_by(ProductStore.product_id==product.id,
                                                                          ProductStore.store_id==store.id).first()
                productstore.store_url = storeData['url']
                productstore.store_price = float(''.join(storeData['price'].split()[1:]).replace(',', ''))
                productstore.store_shipping = storeData['shipping']
                productstore.store_delivery = storeData['delivery']
                productstore.store_cod = storeData['cod']
                productstore.store_emi = storeData['emi']
            else:
                productstore = ProductStore(store_url=storeData['url'],
                                            store_price=float(''.join(storeData['price'].split()[1:]).replace(',', '')),
                                            store_shipping=storeData['shipping'],
                                            store_delivery=storeData['delivery'],
                                            store_cod = storeData['cod'],
                                            store_emi = storeData['emi'])

            productstore.store = store
            productstore.product = product
            self.session.add(productstore)
            self.session.commit()


        # line = json.dumps(dict(item))+ "\n \n \n"
        # self.file.write(line)
        return item
