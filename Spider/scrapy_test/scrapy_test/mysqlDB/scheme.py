from scrapy_test.mysqlDB.operation import Operation

# 以元组的形式返回


def get_keywords(sql):
    operate = Operation()
    operate.connection()
    result = operate.query(sql=sql)
    operate.close()
    return result


def main():
    sql = 'select keyword from scheme'
    result = get_keywords(sql)
    for key in result:
        print(key[0])


if __name__ == '__main__':
    main()