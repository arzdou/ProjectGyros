	db MUNCHLAX

	db 135, 85, 40, 85, 40, 5, 
	;   hp  atk  def  spd  sat  sdf

	db NORMAL, NORMAL ; type
	db 50 ; catch rate
	db 78 ; base exp
	db LEFTOVERS, NO_ITEM ; items
	db GENDER_F12_5 ; gender ratio
	db 100 ; unkown 1
	db 40 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/munchlax/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_SLOW ; growth rate
	dn EGG_NONE, EGG_NONE ; egg groups

	; tm/hm learnset
	tmhm FIRE_PUNCH, ICE_PUNCH, HEADBUTT, BLIZZARD, THUNDER, EARTHQUAKE, TOXIC, DOUBLE_TEAM, FIRE_BLAST, REST, SNORE, PROTECT, MUD_SLAP, ICY_WIND, SANDSTORM, ENDURE, SWAGGER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, HIDDEN_POWER, RAIN_DANCE, SUNNY_DAY, SHADOW_BALL, ROCK_SMASH
	; end
