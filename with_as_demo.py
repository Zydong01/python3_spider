class testWithAs():
    def __enter__(self):
        print("i'm enter!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("i'm exit!")

    def test(self):
        print('我是a')

def get_testWithAs():
    return testWithAs()

if __name__ == '__main__':
    with get_testWithAs() as a:
        
        print('测试')
