	db BIBAREL

	db 79, 85, 60, 60, 55, 71, 
	;   hp  atk  def  spd  sat  sdf

	db NORMAL, WATER ; type
	db 127 ; catch rate
	db 144 ; base exp
	db NO_ITEM, NO_ITEM ; items
	db GENDER_F50 ; gender ratio
	db 100 ; unkown 1
	db 15 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/bibarel/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_MEDIUM_FAST ; growth rate
	dn EGG_WATER_1, EGG_GROUND ; egg groups

	; tm/hm learnset
	tmhm BLIZZARD, HYPER_BEAM, THUNDER, DIG, TOXIC, DOUBLE_TEAM, SWIFT, REST, THIEF, SNORE, PROTECT, MUD_SLAP, ICY_WIND, ENDURE, SWAGGER, FURY_CUTTER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, IRON_TAIL, HIDDEN_POWER, RAIN_DANCE, SUNNY_DAY, SHADOW_BALL, ROCK_SMASH
	; end
