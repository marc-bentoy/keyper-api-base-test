# Keyper API (base test) Endpoints

## POST /api/building
- adds new building row to buildings table
```json
{
    "name": "building-name" // name of the building to add 
}
```

## POST /api/storey 
- adds new storey to stories table
```json
{
    "building_id": 1, // the building id which the storey resides
    "storey": 1 // the nth floor of the building
}
```

## POST /api/room
- adds new room row to rooms table
```json
{
    "building_id": 1, // the building id which the room resides
    "storey_id": 1, // the storey id which the room resides
    "name": "ROOM NAME", // name of the room specified by the organization
    "number": "ROOM NUMBER" // room number specified by the organization
}
```

## POST /api/key
- adds new key row to keys table
```json
{
    "room_id": 1, // specific id of only 1 room 
    "rfid": "04B", // RFID value of the card paired by the key
    "borrow_status": false // borrow status of the key (true if borrowed, false if not)
}
```
- room_id INTEGER, FOREIGN KEY
- rfid TEXT
- borrow_status BOOLEAN

## POST /api/borrow
