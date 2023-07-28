locals {
  lambda_event_payload = {
    "2023/08/02"   = "12:50,07:00,19:30",
    "BRS_USERNAME" = "10773134",
    "BRS_PASSWORD" = "20Diesel08",
    "PLAYER_1"     = "3072", #Niall
    "PLAYER_2"     = "3719", #Ed
    "PLAYER_3"     = "3291", #Dave
    "CLUB_NAME"    = "belvoir",
  }

  tags = {
    Name = "Tee Time Booker"
  }
}