	db SWAMPERT

	db 100, 110, 90, 90, 85, 60, 
	;   hp  atk  def  spd  sat  sdf

	db WATER, GROUND ; type
	db 45 ; catch rate
	; db 268 ; base exp ; ERROR - must be 8 bit
	db 255 ; using high 8-bit value instead
	db NO_ITEM, NO_ITEM ; items
	db GENDER_F12_5 ; gender ratio
	db 100 ; unkown 1
	db 20 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/swampert/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_MEDIUM_SLOW ; growth rate
	dn EGG_MONSTER, EGG_WATER_1 ; egg groups

	; tm/hm learnset
	tmhm ICE_PUNCH, HEADBUTT, ROAR, BLIZZARD, HYPER_BEAM, DIG, TOXIC, DOUBLE_TEAM, DEFENSE_CURL, REST, SNORE, ICY_WIND, ENDURE, ROLLOUT, SWAGGER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, IRON_TAIL, HIDDEN_POWER, RAIN_DANCE, ROCK_SMASH
	; end
