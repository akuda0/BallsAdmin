from keyboard_handlers.handlers import *
from db_handlers.handlers import *
from third_party.ops import *
import configparser


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("back|"):
        await back(query, context)

    elif query.data == 'show_orders':
        await show_orders(query)

    elif query.data == 'confirm_orders':
        pass

    elif query.data == 'edit_db':
        pass

    elif query.data == 'add_item':
        pass

    elif query.data == 'delete_item':
        pass

# TODO: class BALL

class Order:
    def __init__(self, id, ball, type, amount, nick, status, notes):
        self.id = id
        self.ball = ball
        self.type = type
        self.amount = amount
        self.nick = nick
        self.status = status  # paid/not paid
        self.notes = notes

    def change_status(self, status, ball_id):
        config = configparser.ConfigParser()
        config.read_file("cfg_file.ini")
        config["balloon.tmp_trash"]["shaped_balls_trash"]
        connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
        cursor = connection.cursor()
        if status == "paid":
            cursor.execute("REPLACE INTO Orders (status) VALUES (paid)")
        elif status == "delivered":
            cursor.execute(f"INSERT INTO Orders_history (ball, type, amount, nickname, status)"
                           f"VALUES ({cursor.execute("SELECT ball, type, amount, nickname, status"
                                                     f"FROM Orders WHERE id = {ball_id}")})")
            cursor.execute(f"DELETE Orders WHERE id = {ball_id}")
        connection.close()


class Orders:
    def __init__(self):
        self.path = get_db_path()
        self.orders = {"common": [], "shaped": [], "blowup": []}
        self.__get_orders_from_db()

    def __get_orders_from_db(self):
        common_orders, shaped_orders, blowup_orders = get_orders()
        for order_tuple in common_orders:
            order = Order(*order_tuple) # (1, 'common', 'Hello, Kitty', 'latex', 'black', 'hello_kitty_black.jpg', 1, 65, '@akuda0')
            self.orders["common"].append(order)
        for order_tuple in shaped_orders:
            order = Order(*order_tuple)
            self.orders["shaped"].append(order)
        for order_tuple in blowup_orders:
            order = Order(*order_tuple)
            self.orders["blowup"].append(order)


def main():
    application = Application.builder().token("6875313175:AAHB0_46knn6bf4iapEGYVKkcTxBSeCz8pk").build()
    application.add_handler(CommandHandler(["start"], start))
    # application.add_handler(CommandHandler(["orders"], orders))
    application.add_handler(CallbackQueryHandler(button))
    # application.add_handler(MessageHandler(filters.Regex("^\d+$"),order_registrar))  # MessageHandler(filters.Regex("^(Boy|Girl|Other)$")
    application.run_polling()
    application.start()


if __name__ == "__main__":
    # config = configparser.ConfigParser()
    # path_to_config = os.path.join("config", "cfg_file.ini")
    # with open(path_to_config) as cfg_file:
    #     config.read_file(cfg_file)
    #     db_path = config["admin.db"]["db_path"]
    #
    # connection = sqlite3.Connection(db_path)
    # cursor = connection.cursor()
    #
    # s = cursor.execute("SELECT nickname from Orders").fetchall()
    # print(s)
    main()
