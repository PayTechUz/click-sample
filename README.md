# 🔵 Click Implementation

Support Group - <a href="https://t.me/+bYouuOlqt1c3NmYy">Telegram</a><br>
YouTube - <a href="https://www.youtube.com/@paytechuz"> Watch Video</a> (coming soon)<br>
This MVP project helps to implement <a href="https://github.com/PayTechUz/click-pkg">click-pkg</a> (coming soon).

### API Endpoints

- `/click/merchant/` GET: Get a pay link for pay each order:

  ```
  GET: http://127.0.0.1:8000/click/merchant?order_id=12
  ```

  ```json
  {
    "link": "https://my.click.uz/services/pay?service_id=12345&merchant_id=12345&amount=500&transaction_param=12",
    "status": false
  }
  ```

### Merchant endpoint

- `/click/merchant/` POST: includes `PREPARE/COMPLETE` merchant methods that tests on <a href="http://docs.click.uz/wp-content/uploads/2018/05/NEW-CLICK_API.zip">ClickUz Shop-API Application</a>

### Swagger

![image](https://github.com/PayTechUz/click-sample/assets/73847672/c4546bb8-531c-4b2a-99a8-fa5da4935ac2)

### ClickUz Application Test

![image](https://github.com/PayTechUz/click-sample/assets/73847672/4964c951-a48c-4291-b615-5ddc007fd5ef)

# Installation

- 1 - Clone repo
  ```shell
  git clone https://github.com/PayTechUz/click-sample.git
  ```
- 2 - Create a virtual environment and activate
  ```shell
  pip3 install virtualenv
  ```
  ```shell
  virtualenv env
  ```
  ```cmd
  env\Scripts\activate # windows
  ```
  ```shell
  source env/bin/activate # unix-based systems
  ```
- 3 - Change dir into project
  ```shell
  cd click-sample
  ```
- 4 - Install dependencies
  ```shell
  pip3 install -r requirements.txt
  ```
- 5 - Set your environment variables
  ```shell
  cp .sample.env .env # unix-based systems
  ```
- 6 - Run
  ```shell
  python manage.py makemigrations
  ```
  ```shell
  python manage.py migrate
  ```
  ```shell
  python manage.py createsuperuser
  ```
  ```shell
  python manage.py runserver
  ```

# Thanks

- [begyy/ClickUz](https://github.com/begyy/ClickUz)
- [click-llc/click-integration-django](https://github.com/click-llc/click-integration-django)
