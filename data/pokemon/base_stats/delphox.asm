	db DELPHOX

	db 75, 69, 72, 100, 114, 104, 
	;   hp  atk  def  spd  sat  sdf

	db FIRE, PSYCHIC_TYPE ; type
	db 45 ; catch rate
	db 240 ; base exp
	db NO_ITEM, NO_ITEM ; items
	db GENDER_F12_5 ; gender ratio
	db 100 ; unkown 1
	db 20 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/delphox/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_MEDIUM_SLOW ; growth rate
	dn EGG_GROUND, EGG_GROUND ; egg groups

	; tm/hm learnset
	tmhm FIRE_PUNCH, HYPER_BEAM, TOXIC, DOUBLE_TEAM, DREAM_EATER, REST, THIEF, SNORE, PROTECT, SWAGGER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, IRON_TAIL, HIDDEN_POWER, RAIN_DANCE, PSYCH_UP
	; end
