Doug Moyer - Alex Meddin
January 27-28, 2018
BrickHack 4

URL: http://www.schedulr.me/
Test Username: moyer
	 Password: 1234

Project:
	Schedulr (Group Calendar Sharing App)

Features:
	Friends List
	Make Group
	Individual Calendar
	Add event
	Delete event
	Edit event
	Compare 2 calendars
	Compare Group Calendars
	Who’s Free Now?

Calendar integration
	SIS
	Google

Database:
	users
		user_id (primary key)
		username
		password 
	groups
		group_id (primary key)
		group_name
		owner_id
	in_group
		id (primary key)
		group_id 
		user_id
	schedule
		event_id (primary key)
		user_id
		event_name
		start_time
		end_time
