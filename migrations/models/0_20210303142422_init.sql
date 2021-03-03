-- upgrade --
CREATE TYPE order_payment_methods__type AS ENUM ('cash', 'card', 'apple_pay', 'google_pay');

CREATE TABLE IF NOT EXISTS "order_payment_methods" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "type" order_payment_methods__type NOT NULL
);

COMMENT ON TABLE "order_payment_methods" IS 'Модель для описания сущности способа оплаты заказа';

CREATE SEQUENCE IF NOT EXISTS "orders_number_seq";
CREATE TYPE orders__status AS ENUM ('placed', 'completed', 'canceled');

CREATE TABLE IF NOT EXISTS "orders" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "id" UUID NOT NULL  PRIMARY KEY,
    "number" INT NOT NULL UNIQUE DEFAULT nextval('orders_number_seq'),
    "status" orders__status NOT NULL DEFAULT 'placed',
    "comment" VARCHAR(500),
    "business_profile_id" UUID NOT NULL,
    "client_id" UUID NOT NULL,
    "delivery_price" DECIMAL(10,2) NOT NULL,
    "order_price" DECIMAL(10,2) NOT NULL,
    "total_price" DECIMAL(10,2) NOT NULL,
    "payment_method_id" UUID NOT NULL REFERENCES "order_payment_methods" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "orders" IS 'Модель для описания структуры хранения сущностей';

CREATE TABLE IF NOT EXISTS "order_products" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "product_id" UUID NOT NULL,
    "name" VARCHAR(28) NOT NULL,
    "description" VARCHAR(60),
    "price" DECIMAL(10,2) NOT NULL,
    "qty" INT NOT NULL,
    "image_url" VARCHAR(255) NOT NULL,
    "attributes" JSONB,
    "categories" JSONB NOT NULL,
    "catalog_id" UUID NOT NULL,
    "order_id" UUID NOT NULL REFERENCES "orders" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "order_products" IS 'Модель описывающая продукты заказа';
COMMENT ON COLUMN order_products.product_id IS 'Поле для хранения uuid продукта из сервиса каталогов';

CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
