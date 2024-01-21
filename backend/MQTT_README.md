# MQTT topics and messages

## topic buses/driver

### message next_stop

    next_stop?bus=<BUS_ID>

Response:
    
* Default response:

      <STOP_NUMBER>-<STOP_NAME>

* The end of the route:

      end

* The bus is not on the route:

      no route

* No bus with the given ID:

      no bus

### message choose_course

    choose_course?bus=<BUS_ID>&course=<COURSE_NAME>

Response:

    <STOP_NUMBER>-<STOP_NAME>

## topic buses/worker

### message use_card

    use_card?card=<CARD_ID>&bus=<BUS_ID>

Response:

* Worker gets out from the bus:

      <WORKER_BALANCE>

* Worker gets into the bus:

  * Valid card ID:
  
        success

  * Invalid card ID:
  
        error