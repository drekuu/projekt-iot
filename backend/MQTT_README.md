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

    choose_course?bus=<BUS_ID>&course=<COURSE_ID>&direction=<DIRECTION>

DIRECTION argument is 1 (start from the first stop) or 0 (start from the last stop)

Response:

    <STOP_NUMBER>-<STOP_NAME>

## topic buses/worker

### message use_card

    use_card?card=<CARD_ID>&bus=<BUS_ID>

Response:

* Worker gets out from the bus:

      Worker <WORKER_ID> gets out from the bus

* Worker gets into the bus:

      Worker <WORKER_ID> gets into the bus <BUS_ID>