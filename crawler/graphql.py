query = r"""{
  "query": "query PlansAndRooms($accommodationId: AccommodationIdScalar!, $accommodationAmountInput: AccommodationAmountInput!, $hasCheckInDate: Boolean! = false, $onPlans: Boolean! = false, $plansInput: SearchPlansInput! = {}, $plansFirst: Int! = 3, $plansOffset: Int! = 0, $planAmountsInput: PlanAmountInput! = {sortItem: \"1\", sortOrder: \"1\"}, $onRooms: Boolean! = false, $roomsInput: SearchRoomsInput! = {}, $roomsFirst: Int! = 3, $roomsOffset: Int! = 0, $roomAmountsInput: RoomAmountInput! = {sortItem: \"1\", sortOrder: \"1\"}, $amountsAndPlanFirst: Int! = 1, $amountsAndRoomFirst: Int! = 1) {\n  accommodation(accommodationId: $accommodationId) {\n    __typename\n    accommodationId\n    allowInstantDiscount\n    ...PlanListAccommodationAllowInstantDiscount\n    ...RoomListAccommodationAllowInstantDiscount\n    ...AccommodationLowestAmountAccommodation\n    ...AccommodationHeroboxAccommodationLowestAmount\n    ...AccommodationHeroboxAccommodationDisappearingInventory @include(if: $hasCheckInDate)\n    ...AccommodationThemeListAccommodationRecommend\n    searchPlans2(input: $plansInput, first: $plansFirst, offset: $plansOffset) {\n      facet @include(if: $onPlans) {\n        ...AccommodationAvailabilityCalendarSearchPlansFacet\n        ...PlanAndRoomFilterSearchPlansFacet\n      }\n      plans {\n        ...PlanListPlanConnectionAccommodation @include(if: $onPlans)\n        ...RoomPlanMetaPlanConnection @include(if: $onPlans)\n        ...PlanOrRoomChoicePlanConnection\n      }\n    }\n    searchRooms2(input: $roomsInput, first: $roomsFirst, offset: $roomsOffset) {\n      facet @include(if: $onRooms) {\n        ...AccommodationAvailabilityCalendarSearchRoomsFacet\n        ...PlanAndRoomFilterSearchRoomsFacet\n      }\n      rooms {\n        ...AccommodationFaqListRoomConnection @include(if: $onRooms)\n        ...RoomListRoomConnectionAccommodation @include(if: $onRooms)\n        ...RoomPlanMetaRoomConnection @include(if: $onRooms)\n        ...PlanOrRoomChoiceRoomConnection\n      }\n    }\n  }\n}\n\nfragment BaseDiscountDescriptionAmountDetail on AmountDetail {\n  baseDiscount {\n    baseDiscount {\n      rate {\n        settings {\n          rate\n          days\n        }\n        type\n      }\n      expirationTo\n      promotionEntry {\n        id\n      }\n    }\n    appliedRate\n  }\n}\n\nfragment UwanosePointDetailAmount2 on Amount2 {\n  amount\n  point\n  uwanosePoint\n}\n\nfragment AccommodationAmountAmount2 on Amount2 {\n  amount\n  baseDiscountAmount\n  childACount\n  childBCount\n  childCCount\n  childDCount\n  childECount\n  childFCount\n  discountAmount\n  instantPoint\n  instantPointRate\n  lodgingCount\n  peopleCount\n  point\n  pointRate\n  roomCount\n  uwanosePoint\n  plan {\n    meal {\n      code\n      name\n    }\n    sale\n  }\n  details {\n    ...BaseDiscountDescriptionAmountDetail\n  }\n  ...UwanosePointDetailAmount2\n}\n\nfragment AccommodationLowestAmountAccommodation on Accommodation {\n  amount2(input: $accommodationAmountInput) {\n    ...AccommodationAmountAmount2\n    plan {\n      planId\n      checkInTimeFrom\n      checkOutTime\n      attributes {\n        value\n        name\n      }\n      amenities {\n        amenity {\n          id\n          name\n        }\n        available\n      }\n    }\n    room {\n      roomId\n      name\n      beds {\n        count\n        peopleCount\n        width\n        height\n        length\n      }\n      capacityMax\n      attributes {\n        value\n        name\n      }\n      isAmenitiesDisplay\n      amenities {\n        amenity {\n          id\n          name\n        }\n        available\n      }\n      images(first: 50) {\n        url\n        alt\n      }\n    }\n    pointRate\n    instantPointRate\n  }\n}\n\nfragment ThemeAccommodationPersonalizedThemeFeaturedAccommodation on PersonalizedThemeFeaturedAccommodation {\n  accommodation {\n    accommodationId\n    name\n    areaName\n    prefecture {\n      code\n      name\n    }\n    rating2 {\n      average\n    }\n    imageUrls\n  }\n  thumbnailImageUrl\n}\n\nfragment SideSectionItemPersonalizedThemeFeaturedAccommodation on PersonalizedThemeFeaturedAccommodation {\n  ...ThemeAccommodationPersonalizedThemeFeaturedAccommodation\n  accommodation {\n    accommodationId\n    allowInstantDiscount\n    amount2(input: $accommodationAmountInput) {\n      ...AccommodationAmountAmount2\n      peopleCount\n    }\n  }\n}\n\nfragment SideSectionPersonalizedTheme on PersonalizedTheme {\n  themeId\n  name\n  accommodations(first: 10, offset: 0) {\n    edges {\n      node {\n        ...SideSectionItemPersonalizedThemeFeaturedAccommodation\n      }\n    }\n  }\n}\n\nfragment KodawariFilterSearchPlansFacetAccommodation on SearchPlansFacet {\n  meals {\n    __typename\n    count\n    meal {\n      code\n      name\n    }\n  }\n  planAttributes {\n    __typename\n    count\n    planAttribute {\n      name\n      value\n    }\n  }\n  roomAttributes {\n    __typename\n    roomAttribute {\n      name\n      value\n    }\n    count\n  }\n  roomTypes {\n    __typename\n    count\n    roomType {\n      code\n      name\n    }\n  }\n  serviceAttributes {\n    __typename\n    count\n    serviceAttribute {\n      name\n      value\n    }\n  }\n  }\n\nfragment UwanosePointLabelAmount2 on Amount2 {\n  uwanosePoint\n}\n\nfragment PlanListPlan on Plan {\n  planId\n  amounts(input: $planAmountsInput, first: $amountsAndRoomFirst) {\n    edges {\n      node {\n        amount\n        baseDiscountAmount\n        discountAmount\n        point\n        pointRate\n        instantPoint\n        instantPointRate\n        inventory\n        lodgingCount\n        peopleCount\n        childACount\n        childBCount\n        childCCount\n        childDCount\n        childECount\n        childFCount\n        roomCount\n        plan {\n          meal {\n            code\n            name\n          }\n          sale\n        }\n        room {\n          roomId\n          checkInTimeFrom\n          checkInTimeTo\n          checkOutTime\n          attributes {\n            value\n          }\n          images(first: 1) {\n            alt\n            url\n          }\n          meterFrom\n          beds {\n            count\n            peopleCount\n            width\n            height\n            length\n          }\n          capacityMin\n          capacityMax\n          floorPlan\n          floorNumberBottom\n          floorNumberTop\n          name\n          type {\n            code\n            name\n          }\n        }\n        ...AccommodationAmountAmount2\n        ...UwanosePointLabelAmount2\n      }\n    }\n    totalCount\n  }\n  useCheckInOut\n  checkInTimeFrom\n  checkInTimeTo\n  checkOutTime\n  limitedTwoWeeks\n  bookableStartSoon\n  bookableEndSoon\n  meal {\n    code\n    name\n  }\n  memberRank\n  name\n  isIkyuLimit\n  imageUrls(first: 1)\n  uwanosePointVariation\n}\n\nfragment KodawariFilterSearchRoomsFacetAccommodation on SearchRoomsFacet {\n  meals {\n    __typename\n    count\n    meal {\n      code\n      name\n    }\n  }\n  planAttributes {\n    __typename\n    count\n    planAttribute {\n      name\n      value\n    }\n  }\n  roomAttributes {\n    __typename\n    roomAttribute {\n      name\n      value\n    }\n    count\n  }\n  roomTypes {\n    __typename\n    count\n    roomType {\n      code\n      name\n    }\n  }\n  serviceAttributes {\n    __typename\n    count\n    serviceAttribute {\n      name\n      value\n    }\n  }\n  }\n\nfragment RoomListRoom on Room {\n  roomId\n  checkInTimeFrom\n  checkInTimeTo\n  checkOutTime\n  amounts(input: $roomAmountsInput, first: $amountsAndPlanFirst) {\n    edges {\n      node {\n        amount\n        baseDiscountAmount\n        discountAmount\n        point\n        pointRate\n        instantPoint\n        instantPointRate\n        inventory\n        lodgingCount\n        peopleCount\n        childACount\n        childBCount\n        childCCount\n        childDCount\n        childECount\n        childFCount\n        roomCount\n        plan {\n          planId\n          checkInTimeFrom\n          checkInTimeTo\n          checkOutTime\n          useCheckInOut\n          limitedTwoWeeks\n          bookableStartSoon\n          bookableEndSoon\n          meal {\n            code\n            name\n          }\n          memberRank\n          name\n          imageUrls(first: 1)\n          sale\n          uwanosePointVariation\n        }\n        ...AccommodationAmountAmount2\n        ...UwanosePointLabelAmount2\n      }\n    }\n    totalCount\n  }\n  attributes {\n    value\n  }\n  images(first: 99) {\n    alt\n    url\n  }\n  meterFrom\n  beds {\n    count\n    peopleCount\n    width\n    height\n    length\n  }\n  capacityMin\n  capacityMax\n  floorPlan\n  floorNumberBottom\n  floorNumberTop\n  name\n  renewalDate\n  type {\n    code\n    name\n  }\n}\n\nfragment PlanListAccommodationAllowInstantDiscount on Accommodation {\n  allowInstantDiscount\n}\n\nfragment RoomListAccommodationAllowInstantDiscount on Accommodation {\n  allowInstantDiscount\n}\n\nfragment AccommodationHeroboxAccommodationLowestAmount on Accommodation {\n  ...AccommodationLowestAmountAccommodation\n}\n\nfragment AccommodationHeroboxAccommodationDisappearingInventory on Accommodation {\n  disappearingInventory(input: $roomsInput)\n}\n\nfragment AccommodationThemeListAccommodationRecommend on Accommodation {\n  accommodationId\n  personalization {\n    themes(first: 10, offset: 0) {\n      edges {\n        node {\n          themeId\n          name\n          accommodations(first: 10, offset: 0) {\n            edges {\n              node {\n                thumbnailImageUrl\n                accommodation {\n                  accommodationId\n                  allowInstantDiscount\n                  amount2(input: $accommodationAmountInput) {\n                    peopleCount\n                    ...AccommodationAmountAmount2\n                  }\n                }\n                ...ThemeAccommodationPersonalizedThemeFeaturedAccommodation\n              }\n            }\n          }\n          ...SideSectionPersonalizedTheme\n        }\n      }\n    }\n  }\n}\n\nfragment AccommodationAvailabilityCalendarSearchPlansFacet on SearchPlansFacet {\n  ...KodawariFilterSearchPlansFacetAccommodation\n}\n\nfragment PlanAndRoomFilterSearchPlansFacet on SearchPlansFacet {\n  ...KodawariFilterSearchPlansFacetAccommodation\n}\n\nfragment PlanListPlanConnectionAccommodation on PlanConnection {\n  __typename\n  edges @include(if: $onPlans) {\n    node {\n      planId\n      bookableStartSoon\n      bookableEndSoon\n      limitedTwoWeeks\n      memberRank\n      uwanosePointVariation\n      ...PlanListPlan\n    }\n  }\n  totalCount\n}\n\nfragment RoomPlanMetaPlanConnection on PlanConnection {\n  edges {\n    node {\n      planId\n      amounts(input: $planAmountsInput, first: $amountsAndRoomFirst) {\n        edges {\n          node {\n            room {\n              roomId\n              images(first: 1) {\n                alt\n                url\n              }\n            }\n          }\n        }\n      }\n      imageUrls(first: 1)\n    }\n  }\n}\n\nfragment PlanOrRoomChoicePlanConnection on PlanConnection {\n  totalCount\n}\n\nfragment AccommodationAvailabilityCalendarSearchRoomsFacet on SearchRoomsFacet {\n  ...KodawariFilterSearchRoomsFacetAccommodation\n}\n\nfragment PlanAndRoomFilterSearchRoomsFacet on SearchRoomsFacet {\n  ...KodawariFilterSearchRoomsFacetAccommodation\n}\n\nfragment AccommodationFaqListRoomConnection on RoomConnection {\n  edges {\n    node {\n      attributes {\n        value\n      }\n    }\n  }\n}\n\nfragment RoomListRoomConnectionAccommodation on RoomConnection {\n  __typename\n  edges @include(if: $onRooms) {\n    node {\n      roomId\n      ...RoomListRoom\n    }\n  }\n  totalCount\n}\n\nfragment RoomPlanMetaRoomConnection on RoomConnection {\n  edges {\n    node {\n      roomId\n      amounts(input: $roomAmountsInput, first: $amountsAndPlanFirst) {\n        edges {\n          node {\n            plan {\n              planId\n              imageUrls(first: 1)\n            }\n          }\n        }\n      }\n      images(first: 99) {\n        alt\n        url\n      }\n    }\n  }\n}\n\nfragment PlanOrRoomChoiceRoomConnection on RoomConnection {\n  totalCount\n}",
  "variables": {
    "accommodationId": "{hotel_id}",
    "hasCheckInDate": true,
    "accommodationAmountInput": {
      "checkInDate": "{checkin}",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": {ppc},
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1"
    },
    "onPlans": false,
    "plansInput": {
      "checkInDate": "{checkin}",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": {ppc},
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "planAmountsInput": {
      "checkInDate": "{checkin}",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": {ppc},
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1"
    },
    "plansFirst": 10,
    "onRooms": true,
    "roomsInput": {
      "checkInDate": "{checkin}",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": {ppc},
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "roomAmountsInput": {
      "checkInDate": "{checkin}",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": {ppc},
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "roomsFirst": 999,
    "amountsAndPlanFirst": {plan_count},
    "amountsAndRoomFirst": {room_count}
  },
  "operationName": "PlansAndRooms"
}"""

query2 = r"""
{
  "query": "query PlansAndRooms($accommodationId: AccommodationIdScalar!, $accommodationAmountInput: AccommodationAmountInput!, $hasCheckInDate: Boolean! = false, $onPlans: Boolean! = false, $plansInput: SearchPlansInput! = {}, $plansFirst: Int! = 3, $plansOffset: Int! = 0, $planAmountsInput: PlanAmountInput! = {sortItem: \"1\", sortOrder: \"1\"}, $onRooms: Boolean! = false, $roomsInput: SearchRoomsInput! = {}, $roomsFirst: Int! = 3, $roomsOffset: Int! = 0, $roomAmountsInput: RoomAmountInput! = {sortItem: \"1\", sortOrder: \"1\"}, $amountsAndPlanFirst: Int! = 1, $amountsAndRoomFirst: Int! = 1) {\n  accommodation(accommodationId: $accommodationId) {\n    __typename\n    accommodationId\n    allowInstantDiscount\n    ...PlanListAccommodationAllowInstantDiscount\n    ...RoomListAccommodationAllowInstantDiscount\n    ...AccommodationLowestAmountAccommodation\n    ...AccommodationHeroboxAccommodationLowestAmount\n    ...AccommodationHeroboxAccommodationDisappearingInventory @include(if: $hasCheckInDate)\n    ...AccommodationThemeListAccommodationRecommend\n    searchPlans2(input: $plansInput, first: $plansFirst, offset: $plansOffset) {\n      facet @include(if: $onPlans) {\n        ...AccommodationAvailabilityCalendarSearchPlansFacet\n        ...PlanAndRoomFilterSearchPlansFacet\n      }\n      plans {\n        ...PlanListPlanConnectionAccommodation @include(if: $onPlans)\n        ...RoomPlanMetaPlanConnection @include(if: $onPlans)\n        ...PlanOrRoomChoicePlanConnection\n      }\n    }\n    searchRooms2(input: $roomsInput, first: $roomsFirst, offset: $roomsOffset) {\n      facet @include(if: $onRooms) {\n        ...AccommodationAvailabilityCalendarSearchRoomsFacet\n        ...PlanAndRoomFilterSearchRoomsFacet\n      }\n      rooms {\n        ...AccommodationFaqListRoomConnection @include(if: $onRooms)\n        ...RoomListRoomConnectionAccommodation @include(if: $onRooms)\n        ...RoomPlanMetaRoomConnection @include(if: $onRooms)\n        ...PlanOrRoomChoiceRoomConnection\n      }\n    }\n  }\n}\n\nfragment BaseDiscountDescriptionAmountDetail on AmountDetail {\n  baseDiscount {\n    baseDiscount {\n      rate {\n        settings {\n          rate\n          days\n        }\n        type\n      }\n      expirationTo\n      promotionEntry {\n        id\n      }\n    }\n    appliedRate\n  }\n}\n\nfragment UwanosePointDetailAmount2 on Amount2 {\n  amount\n  point\n  uwanosePoint\n}\n\nfragment AccommodationAmountAmount2 on Amount2 {\n  amount\n  baseDiscountAmount\n  childACount\n  childBCount\n  childCCount\n  childDCount\n  childECount\n  childFCount\n  discountAmount\n  instantPoint\n  instantPointRate\n  lodgingCount\n  peopleCount\n  point\n  pointRate\n  roomCount\n  uwanosePoint\n  plan {\n    meal {\n      code\n      name\n    }\n    sale\n  }\n  details {\n    ...BaseDiscountDescriptionAmountDetail\n  }\n  ...UwanosePointDetailAmount2\n}\n\nfragment AccommodationLowestAmountAccommodation on Accommodation {\n  amount2(input: $accommodationAmountInput) {\n    ...AccommodationAmountAmount2\n    plan {\n      planId\n      checkInTimeFrom\n      checkOutTime\n      attributes {\n        value\n        name\n      }\n      amenities {\n        amenity {\n          id\n          name\n        }\n        available\n      }\n    }\n    room {\n      roomId\n      name\n      beds {\n        count\n        peopleCount\n        width\n        height\n        length\n      }\n      capacityMax\n      attributes {\n        value\n        name\n      }\n      isAmenitiesDisplay\n      amenities {\n        amenity {\n          id\n          name\n        }\n        available\n      }\n      images(first: 50) {\n        url\n        alt\n      }\n    }\n    pointRate\n    instantPointRate\n  }\n}\n\nfragment ThemeAccommodationPersonalizedThemeFeaturedAccommodation on PersonalizedThemeFeaturedAccommodation {\n  accommodation {\n    accommodationId\n    name\n    areaName\n    prefecture {\n      code\n      name\n    }\n    rating2 {\n      average\n    }\n    imageUrls\n  }\n  thumbnailImageUrl\n}\n\nfragment SideSectionItemPersonalizedThemeFeaturedAccommodation on PersonalizedThemeFeaturedAccommodation {\n  ...ThemeAccommodationPersonalizedThemeFeaturedAccommodation\n  accommodation {\n    accommodationId\n    allowInstantDiscount\n    amount2(input: $accommodationAmountInput) {\n      ...AccommodationAmountAmount2\n      peopleCount\n    }\n  }\n}\n\nfragment SideSectionPersonalizedTheme on PersonalizedTheme {\n  themeId\n  name\n  accommodations(first: 10, offset: 0) {\n    edges {\n      node {\n        ...SideSectionItemPersonalizedThemeFeaturedAccommodation\n      }\n    }\n  }\n}\n\nfragment KodawariFilterSearchPlansFacetAccommodation on SearchPlansFacet {\n  meals {\n    __typename\n    count\n    meal {\n      code\n      name\n    }\n  }\n  planAttributes {\n    __typename\n    count\n    planAttribute {\n      name\n      value\n    }\n  }\n  roomAttributes {\n    __typename\n    roomAttribute {\n      name\n      value\n    }\n    count\n  }\n  roomTypes {\n    __typename\n    count\n    roomType {\n      code\n      name\n    }\n  }\n  serviceAttributes {\n    __typename\n    count\n    serviceAttribute {\n      name\n      value\n    }\n  }\n  }\n\nfragment UwanosePointLabelAmount2 on Amount2 {\n  uwanosePoint\n}\n\nfragment PlanListPlan on Plan {\n  planId\n  amounts(input: $planAmountsInput, first: $amountsAndRoomFirst) {\n    edges {\n      node {\n        amount\n        baseDiscountAmount\n        discountAmount\n        point\n        pointRate\n        instantPoint\n        instantPointRate\n        inventory\n        lodgingCount\n        peopleCount\n        childACount\n        childBCount\n        childCCount\n        childDCount\n        childECount\n        childFCount\n        roomCount\n        plan {\n          meal {\n            code\n            name\n          }\n          sale\n        }\n        room {\n          roomId\n          checkInTimeFrom\n          checkInTimeTo\n          checkOutTime\n          attributes {\n            value\n          }\n          images(first: 1) {\n            alt\n            url\n          }\n          meterFrom\n          beds {\n            count\n            peopleCount\n            width\n            height\n            length\n          }\n          capacityMin\n          capacityMax\n          floorPlan\n          floorNumberBottom\n          floorNumberTop\n          name\n          type {\n            code\n            name\n          }\n        }\n        ...AccommodationAmountAmount2\n        ...UwanosePointLabelAmount2\n      }\n    }\n    totalCount\n  }\n  useCheckInOut\n  checkInTimeFrom\n  checkInTimeTo\n  checkOutTime\n  limitedTwoWeeks\n  bookableStartSoon\n  bookableEndSoon\n  meal {\n    code\n    name\n  }\n  memberRank\n  name\n  isIkyuLimit\n  imageUrls(first: 1)\n  uwanosePointVariation\n}\n\nfragment KodawariFilterSearchRoomsFacetAccommodation on SearchRoomsFacet {\n  meals {\n    __typename\n    count\n    meal {\n      code\n      name\n    }\n  }\n  planAttributes {\n    __typename\n    count\n    planAttribute {\n      name\n      value\n    }\n  }\n  roomAttributes {\n    __typename\n    roomAttribute {\n      name\n      value\n    }\n    count\n  }\n  roomTypes {\n    __typename\n    count\n    roomType {\n      code\n      name\n    }\n  }\n  serviceAttributes {\n    __typename\n    count\n    serviceAttribute {\n      name\n      value\n    }\n  }\n  }\n\nfragment RoomListRoom on Room {\n  roomId\n  checkInTimeFrom\n  checkInTimeTo\n  checkOutTime\n  amounts(input: $roomAmountsInput, first: $amountsAndPlanFirst) {\n    edges {\n      node {\n        amount\n        baseDiscountAmount\n        discountAmount\n        point\n        pointRate\n        instantPoint\n        instantPointRate\n        inventory\n        lodgingCount\n        peopleCount\n        childACount\n        childBCount\n        childCCount\n        childDCount\n        childECount\n        childFCount\n        roomCount\n        plan {\n          planId\n          checkInTimeFrom\n          checkInTimeTo\n          checkOutTime\n          useCheckInOut\n          limitedTwoWeeks\n          bookableStartSoon\n          bookableEndSoon\n          meal {\n            code\n            name\n          }\n          memberRank\n          name\n          imageUrls(first: 1)\n          sale\n          uwanosePointVariation\n        }\n        ...AccommodationAmountAmount2\n        ...UwanosePointLabelAmount2\n      }\n    }\n    totalCount\n  }\n  attributes {\n    value\n  }\n  images(first: 99) {\n    alt\n    url\n  }\n  meterFrom\n  beds {\n    count\n    peopleCount\n    width\n    height\n    length\n  }\n  capacityMin\n  capacityMax\n  floorPlan\n  floorNumberBottom\n  floorNumberTop\n  name\n  renewalDate\n  type {\n    code\n    name\n  }\n}\n\nfragment PlanListAccommodationAllowInstantDiscount on Accommodation {\n  allowInstantDiscount\n}\n\nfragment RoomListAccommodationAllowInstantDiscount on Accommodation {\n  allowInstantDiscount\n}\n\nfragment AccommodationHeroboxAccommodationLowestAmount on Accommodation {\n  ...AccommodationLowestAmountAccommodation\n}\n\nfragment AccommodationHeroboxAccommodationDisappearingInventory on Accommodation {\n  disappearingInventory(input: $roomsInput)\n}\n\nfragment AccommodationThemeListAccommodationRecommend on Accommodation {\n  accommodationId\n  personalization {\n    themes(first: 10, offset: 0) {\n      edges {\n        node {\n          themeId\n          name\n          accommodations(first: 10, offset: 0) {\n            edges {\n              node {\n                thumbnailImageUrl\n                accommodation {\n                  accommodationId\n                  allowInstantDiscount\n                  amount2(input: $accommodationAmountInput) {\n                    peopleCount\n                    ...AccommodationAmountAmount2\n                  }\n                }\n                ...ThemeAccommodationPersonalizedThemeFeaturedAccommodation\n              }\n            }\n          }\n          ...SideSectionPersonalizedTheme\n        }\n      }\n    }\n  }\n}\n\nfragment AccommodationAvailabilityCalendarSearchPlansFacet on SearchPlansFacet {\n  ...KodawariFilterSearchPlansFacetAccommodation\n}\n\nfragment PlanAndRoomFilterSearchPlansFacet on SearchPlansFacet {\n  ...KodawariFilterSearchPlansFacetAccommodation\n}\n\nfragment PlanListPlanConnectionAccommodation on PlanConnection {\n  __typename\n  edges @include(if: $onPlans) {\n    node {\n      planId\n      bookableStartSoon\n      bookableEndSoon\n      limitedTwoWeeks\n      memberRank\n      uwanosePointVariation\n      ...PlanListPlan\n    }\n  }\n  totalCount\n}\n\nfragment RoomPlanMetaPlanConnection on PlanConnection {\n  edges {\n    node {\n      planId\n      amounts(input: $planAmountsInput, first: $amountsAndRoomFirst) {\n        edges {\n          node {\n            room {\n              roomId\n              images(first: 1) {\n                alt\n                url\n              }\n            }\n          }\n        }\n      }\n      imageUrls(first: 1)\n    }\n  }\n}\n\nfragment PlanOrRoomChoicePlanConnection on PlanConnection {\n  totalCount\n}\n\nfragment AccommodationAvailabilityCalendarSearchRoomsFacet on SearchRoomsFacet {\n  ...KodawariFilterSearchRoomsFacetAccommodation\n}\n\nfragment PlanAndRoomFilterSearchRoomsFacet on SearchRoomsFacet {\n  ...KodawariFilterSearchRoomsFacetAccommodation\n}\n\nfragment AccommodationFaqListRoomConnection on RoomConnection {\n  edges {\n    node {\n      attributes {\n        value\n      }\n    }\n  }\n}\n\nfragment RoomListRoomConnectionAccommodation on RoomConnection {\n  __typename\n  edges @include(if: $onRooms) {\n    node {\n      roomId\n      ...RoomListRoom\n    }\n  }\n  totalCount\n}\n\nfragment RoomPlanMetaRoomConnection on RoomConnection {\n  edges {\n    node {\n      roomId\n      amounts(input: $roomAmountsInput, first: $amountsAndPlanFirst) {\n        edges {\n          node {\n            plan {\n              planId\n              imageUrls(first: 1)\n            }\n          }\n        }\n      }\n      images(first: 99) {\n        alt\n        url\n      }\n    }\n  }\n}\n\nfragment PlanOrRoomChoiceRoomConnection on RoomConnection {\n  totalCount\n}",
  "variables": {
    "accommodationId": "00002956",
    "hasCheckInDate": true,
    "accommodationAmountInput": {
      "checkInDate": "2024-04-30",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": 2,
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1"
    },
    "onPlans": false,
    "plansInput": {
      "checkInDate": "2024-04-30",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": 2,
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "planAmountsInput": {
      "checkInDate": "2024-04-30",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": 2,
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1"
    },
    "plansFirst": 10,
    "onRooms": true,
    "roomsInput": {
      "checkInDate": "2024-04-30",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": 2,
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "roomAmountsInput": {
      "checkInDate": "2024-04-30",
      "discount": true,
      "lodgingCount": 1,
      "peopleCount": 2,
      "roomCount": 1,
      "searchType": "1",
      "sortItem": "1",
      "sortOrder": "1",
      "bookable": "ALL",
      "preferBookable": true
    },
    "roomsFirst": 999,
    "amountsAndPlanFirst": 2,
    "amountsAndRoomFirst": 2
  },
  "operationName": "PlansAndRooms"
}"""