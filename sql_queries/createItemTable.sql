CREATE TABLE IF NOT EXISTS "Items" (
	"item_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"image"	TEXT NOT NULL,
	"cost"	REAL NOT NULL,
	"manufacturer"	TEXT NOT NULL,
	PRIMARY KEY("item_id" AUTOINCREMENT)
);