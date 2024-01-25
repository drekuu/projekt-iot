# MQTT topics and messages

## topic buses/driver

### message next_stop

    next_stop?bus=<BUS_ID>

### message choose_course

    choose_course?bus=<BUS_ID>&course=<COURSE_NAME>

## topic buses/worker

### message use_card

    use_card?card=<CARD_ID>&bus=<BUS_ID>

Response (topic response/success):

* Worker gets out from the bus:

      Balance after ride: <WORKER_BALANCE>.

* Worker gets into the bus:

  * Valid card ID:
  
        Card validated succesfully.

  * Invalid card ID:
  
        Invalid card.