	db GOGOAT

	db 123, 100, 62, 81, 97, 68, 
	;   hp  atk  def  spd  sat  sdf

	db GRASS, GRASS ; type
	db 45 ; catch rate
	db 186 ; base exp
	db NO_ITEM, NO_ITEM ; items
	db GENDER_F50 ; gender ratio
	db 100 ; unkown 1
	db 20 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/gogoat/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_MEDIUM_FAST ; growth rate
	dn EGG_GROUND, EGG_GROUND ; egg groups

	; tm/hm learnset
	tmhm ROAR, HYPER_BEAM, DIG, TOXIC, DOUBLE_TEAM, REST, SNORE, PROTECT, GIGA_DRAIN, SWAGGER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, IRON_TAIL, HIDDEN_POWER, RAIN_DANCE, SUNNY_DAY, ROCK_SMASH
	; end
