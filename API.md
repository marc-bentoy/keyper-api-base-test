# Keyper API (base test) Endpoints

- POST `/api/building` 
  - creates new buildings table *if not created* with a JSON payload:
  ```json
  {
    "name": "building-name"
  }
  ```

- POST `/api/storey` 
    - creates new stories table *if not created* that represents a building storey/floor
    - with a JSON payload:
    ```json
    {
        "building": 1, // building id from the specified building
        "storey": 1, // the nth floor of the building
    }
    ```

- POST `/api/room`
    - creates new rooms table *if not created* that represents the room in a specified building and specified storey
    - with a JSON payload:
    ```json
    {
        "building": 1, // the building id which the room resides
        "storey": 1, // the storey id which the room resides
        "name": "ROOM NAME", // name of the room specified by the organization
        "number": "ROOM NUMBER" // room number specified by the organization
    }
    ```

- POST `/api/key`
    - creates new keys table *if not created* that represents the key of a specific room
    - with JSON payload:
    ```json
    {
        "room": 1, // specific id of only 1 room 
        "rfid": "04B", // RFID value of the card paired by the key
    }
    ```

- POST `/api/borrow`
    - creates a new borrow_list table *if not yet created*
    - updates the borrowed status of the speicified key to `true`
    - with a JSON payload:
    ```json
    {
        "key": 1, // specific id of only 1 room 
        "date": "04-29-2023 9:03:00" // (optional payload) can be set depending on the request or can be left blank to add the current time and date
    }
    ```

- POST `/api/return`
    - creates a new return_list table *if not yet created*
    - updates the borrowed status of the speicified key to `false`
    - with a JSON payload:
    ```json
    {
        "key": 1, // specific id of only 1 room 
        "date": "04-29-2023 9:03:00" // (optional payload) can be set depending on the request or can be left blank to add the current time and date
    }
    ```