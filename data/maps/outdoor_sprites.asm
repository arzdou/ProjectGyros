; Valid sprite IDs for each map group.
; Maps with environment ROUTE or TOWN can only use these sprites.

OutdoorSprites:
; entries correspond to MAPGROUP_* constants
	table_width 2, OutdoorSprites
	dw CableClubGroupSprites
	dw BattleTowerGroupSprites
	dw NewBarkGroupSprites
	dw IndigoGroupSprites
	assert_table_length NUM_MAP_GROUPS



CableClubGroupSprites:
BattleTowerGroupSprites:
NewBarkGroupSprites:
IndigoGroupSprites:
	db SPRITE_COOLTRAINER_M
	db SPRITE_COOLTRAINER_F
	db SPRITE_BUG_CATCHER
	db SPRITE_TWIN
	db SPRITE_YOUNGSTER
	db SPRITE_LASS
	db SPRITE_TEACHER
	db SPRITE_BEAUTY
	db SPRITE_POKEFAN_M
	; max 9 of 9 walking sprites

	db SPRITE_SUICUNE
	db SPRITE_SILVER_TROPHY
	db SPRITE_FAMICOM
	db SPRITE_POKEDEX
	db SPRITE_WILL
	db SPRITE_KAREN
	db SPRITE_NURSE
	db SPRITE_OLD_LINK_RECEPTIONIST
	db SPRITE_BIG_LAPRAS
	db SPRITE_BIG_ONIX
	db SPRITE_SUDOWOODO
	db SPRITE_BIG_SNORLAX
	db SPRITE_POKE_BALL
	db 0 ; end
