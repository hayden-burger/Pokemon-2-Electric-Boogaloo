#Hayden Burger, Corinne Desroches, David Lee
#OA 3302 Simulation Modeling
#May 2024
#Pokemon module

#import statements
import numpy as np
import pandas as pd
import random
import copy
# set pandas copy on write to be true
pd.set_option("mode.copy_on_write", True)

#---------------------------------------------------------------------------------
#Read Data 
###################################
#Pokemon_df:
#grab data
Pokemon_df = pd.read_csv('Input_data_files/pokemon.csv')
columns_to_drop = ['abilities', 'base_egg_steps','base_happiness','capture_rate', 'japanese_name', 'percentage_male', 'is_legendary']
Pokemon_df.drop(columns_to_drop, axis=1, inplace=True)

# combine the multiplier columns together
against_columns = list(Pokemon_df.columns[0:18])

# Create a list of columns in correct order
new_order = ['name'] + ['classfication'] + ['generation'] + ['type1'] + ['type2']+ ['hp'] + ['speed'] + ['attack'] + ['sp_attack']+ ['defense'] + ['sp_defense'] + ['base_total'] + ['experience_growth'] + ['height_m'] + ['weight_kg'] + ['pokedex_number'] + against_columns

# Reorder the DataFrame columns
Pokemon_df = Pokemon_df[new_order]

# take all string columns to lowercase
Pokemon_df.loc[:,['name', 'classfication', 'type1', 'type2']] = Pokemon_df.loc[:,['name', 'classfication', 'type1', 'type2']].apply(lambda x: x.str.lower())

#Replace Null values with 0
Pokemon_df.fillna(0)

#isolates gen 1 pokemon
gen1 = np.where(Pokemon_df['generation'] == 1)
Pokemon_df = Pokemon_df.iloc[gen1]

# # change nidoran♂ to nidoran-m
Pokemon_df.loc[:,'name'] = Pokemon_df.loc[:,'name'].replace('nidoran♂','nidoran-m')
# # change nidoran♀ to nidoran-f
Pokemon_df.loc[:,'name'] = Pokemon_df.loc[:,'name'].replace('nidoran♀','nidoran-f')

# set Pokemon name to index
Pokemon_df.set_index('name',inplace=True)

# add sprites for each pokemon
base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork"
Pokemon_df['image_url'] = Pokemon_df['pokedex_number'].apply(lambda x: f"{base_url}/{x}.png")

# edit stats for level
stats = ['hp', 'speed', 'attack', 'sp_attack', 'defense', 'sp_defense']
Pokemon_level = 50
Pokemon_df.head()
for pokemon in Pokemon_df.index:
    for stat in stats:
        if stat == 'hp':
            Pokemon_df.loc[pokemon, stat] = int(((Pokemon_df.loc[pokemon, stat] * 2) * Pokemon_level / 100) + Pokemon_level + 10)
        else:
            Pokemon_df.loc[pokemon, stat] = int(((Pokemon_df.loc[pokemon, stat] * 2) * Pokemon_level / 100)+ 5)

##################################
#Moveset_df/ L1_moves:
# read in the 1st moveset csv
Moveset_df = pd.read_csv('Input_data_files/Move_set_per_pokemon.csv')

#Create a new dataset L1_moves for all moves of level 1
#array of all indexes with level = 1
moves = np.where(Moveset_df['level'] <= Pokemon_level)
#new dataset indexed by array of indexes
L1_moves = Moveset_df.iloc[moves]
# reindex after truncation
L1_moves.index = (range(len(L1_moves)))
# take all string columns to lowercase
L1_moves.loc[:,['name', 'move', 'type']] = L1_moves.loc[:,['name', 'move', 'type']].apply(lambda x: x.str.lower())
#remove all % from accuracy
L1_moves.loc[:,['accuracy']] = L1_moves.loc[:,['accuracy']].apply(lambda x: x.str.strip('%'))
# replace all - power and pp values with zeros
L1_moves.loc[:,['power', 'pp']] = L1_moves.loc[:,['power', 'pp']].replace('—','0')
L1_moves.loc[:,['accuracy']] = L1_moves.loc[:,['accuracy']].replace('—','_')
# correct accuracy for jynx pound PP from 3500% to 35
L1_moves.loc[np.where(L1_moves['move'] == 'pound')[0], ['pp']] = L1_moves.loc[np.where(L1_moves['move'] == 'pound')[0], ['pp']].replace('3500%',35)
# correct accuracy for Mew Swift from underscore to infinity (999999)
L1_moves.loc[np.where(L1_moves['move'] == 'swift')[0], ['accuracy']] = 999999
# typecast values to int
L1_moves['power'] = pd.to_numeric(L1_moves['power'])
L1_moves['pp'] = pd.to_numeric(L1_moves['pp'])
#change name farfetchd to farfetch'd and mr-mime to mr. mime
L1_moves.loc[:,['name']] = L1_moves.loc[:,['name']].replace('farfetchd',"farfetch'd")
L1_moves.loc[:,['name']] = L1_moves.loc[:,['name']].replace('mr-mime',"mr. mime")
# change 'smoke screen' to 'smokescreen', 'vicegrip' to 'vise grip', 'hi jump kick' to 'high jump kick', and 'self-destruct' to 'self destruct'
L1_moves.loc[:,['move']] = L1_moves.loc[:,['move']].replace('smoke screen','smokescreen')
L1_moves.loc[:,['move']] = L1_moves.loc[:,['move']].replace('vice grip','vise grip')
L1_moves.loc[:,['move']] = L1_moves.loc[:,['move']].replace('vicegrip','vise grip')
L1_moves.loc[:,['move']] = L1_moves.loc[:,['move']].replace('hi jump kick','high jump kick')
L1_moves.loc[:,['move']] = L1_moves.loc[:,['move']].replace('self destruct','self-destruct')

# add the move 'struggle' to the L1_moves dataframe so that it is kept on the merge later.
struggle_row = pd.DataFrame([{'name': 'any', 'level': 1, 'move': 'struggle', 'type': 'normal', 'power': 50, 'accuracy': 100, 'pp': 999}])
L1_moves = pd.concat((L1_moves, struggle_row), ignore_index=True)

##############################################
#AMoveset:
# read in 'Moveset.csv', make all columns lowercase, drop the tm column, and pull just generation 1 moves
AMoveset = pd.read_csv('Input_data_files/Moveset.csv')
AMoveset.rename(str.lower, axis='columns', inplace=True)
AMoveset.rename(columns={'name': 'move'}, inplace=True)
AMoveset.rename(columns={'acc': 'accuracy'}, inplace=True)
AMoveset.rename(columns={'prob.(%)': 'effect_prob'}, inplace=True)
AMoveset.drop(['tm'],axis = 1, inplace=True)
gen1moves = np.where(AMoveset['gen'] == 1)
AMoveset = AMoveset.iloc[gen1moves]

# take all string values and make them lowercase for columns whose values are strings
AMoveset.loc[:,['move', 'type', 'category', 'effect']] = AMoveset.loc[:,['move', 'type', 'category', 'effect']].apply(lambda x: x.str.lower())
# replace all - values with zeros except for accuracy
AMoveset.loc[:,['power', 'pp', 'effect_prob', 'gen']] = AMoveset.loc[:,['power', 'pp', 'effect_prob', 'gen']].replace('-','0')
# replace all - values with _ for accuracy
AMoveset['accuracy'] = AMoveset['accuracy'].replace('-','_')
# replace inf with 999999 (large number)
AMoveset['accuracy'] = AMoveset['accuracy'].replace('∞','999999')
# replace 0 with 100 (large number)
AMoveset['effect_prob'] = AMoveset['effect_prob'].replace('0','100')

# typecast values to int
AMoveset['power'] = AMoveset['power'].astype(int)
AMoveset['pp'] = AMoveset['pp'].astype(int)

# Correct spelling from "vice grip" to 'vise grip' and 'sonic boom' to 'sonicboom'
AMoveset.loc[:,['move']] = AMoveset.loc[:,['move']].replace('vice grip','vise grip')
AMoveset.loc[:,['move']] = AMoveset.loc[:,['move']].replace('sonic boom','sonicboom')

# Correct accuracy for psywave to 80
AMoveset.loc[np.where(AMoveset['move'] == 'psywave')[0], ['accuracy']] = 80
# Correct accuracy for fissure, horn drill, and guillotine to 30
AMoveset.loc[AMoveset['move'].isin(['fissure', 'horn drill', 'guillotine']), 'accuracy'] = 30
# Correct PP for clamp to 15
AMoveset.loc[AMoveset['move'].isin(['clamp']), 'pp'] = 15
# Correct PP for growth and recover to 20
AMoveset.loc[AMoveset['move'].isin(['growth', 'recover']), 'pp'] = 20

# sort by name to put back into alphabetical order
AMovesetSorted = AMoveset.sort_values(by='move')
# reset the index values
AMovesetSorted.index = (range(len(AMovesetSorted)))

AMoveset = AMovesetSorted

####################################################
#Merge movesets into 1 Dataframe
# merge the move set databases into one dataframe
merged_moves_df = pd.merge(L1_moves,AMoveset.loc[:,['move', 'category', 'effect', 'effect_prob', 'gen']], on='move', how='left')
merged_moves_df['gen'] = merged_moves_df['gen'].astype('Int64')
merged_moves_df['effect_prob'] = merged_moves_df['effect_prob'].astype('Int64')
#get rid of duplicate moves with different levels
mm_columns = list(merged_moves_df.columns)
mm_columns.remove('level')
merged_moves_df.drop_duplicates(subset = mm_columns,keep='last',inplace=True)

#--------------------------------------------------------------------------------
def verboseprint(printstatement,verbose):
    '''Prints a statement only if boolean argument is true'''
    if verbose:
        print(printstatement)

#-------------------------------------------------------------------------------
##Pokemon Class:
class Pokemon:
    '''A Class that contains traits for a single pokemon'''

    def __init__(self,name):
        '''Initialize an individual pokemon by name'''
        self.name = name
        #grabs a row from Pokemon_df to reference
        self.individual_df = Pokemon_df.loc[name]
        self.level = Pokemon_level

        #Base stats
        self.start_speed = self.individual_df['speed']
        self.start_attack = self.individual_df['attack']
        self.start_defense = self.individual_df['defense']
        self.start_sp_attack = self.individual_df['sp_attack']
        self.start_sp_defense = self.individual_df['sp_defense']
        self.start_hp = self.individual_df['hp']

        #Base types:
        type1 = self.individual_df['type1']
        type2 = self.individual_df['type2']
        self.start_types = {1:type1} #dictionary of types
        #Includes a second type in dictionary only if it's not 0 (null)
        if type2 != 0:
            self.start_types[2] = type2

        #Damage Multiplier
        #NOTE! this is a multiplier for the damage TAKEN, not dealt
        #Grab all columns of 'against_blank' format and remove 'against_'
        against = self.individual_df.index.str.contains('against_')
        type_advantages_df = self.individual_df[against]
        type_advantages_df.index = type_advantages_df.index.str.replace('against_','')
        #replace 'fight' with 'fighting' to match the pokemon/move type
        type_advantages_df['fighting']=type_advantages_df.pop('fight')
        #create a dictionary of damage multipliers by the type of move
        self.start_damage_multiplier = type_advantages_df.to_dict()

        #Available Moveset at Level 1
        pokemon = np.where(merged_moves_df['name'] == name) #selects pokemon's moves
        pokemon_moves = merged_moves_df.iloc[pokemon] #dataframe of those moves
        pokemon_moves.set_index('move',inplace = True) #sets the moves as the index
        self.start_moveset = {} #dictionary of available moves
        for move in pokemon_moves.index:
        #Each move has a dictionary of type, power, accuracy, pp, effect, and effect prob
            self.start_moveset[move] = {'type':pokemon_moves.loc[move]['type'],\
                             'power':pokemon_moves.loc[move]['power'],\
                             'accuracy':pokemon_moves.loc[move]['accuracy'],\
                             'pp':pokemon_moves.loc[move]['pp'],\
                             'category':pokemon_moves.loc[move]['category'],\
                             'effect':pokemon_moves.loc[move]['effect'],\
                             'effect_prob': pokemon_moves.loc[move]['effect_prob']/100}

        #statuses have stages between -6 to 6 and each corresponds with a multiplier
        #eg if attack is in stage -6, all damage will be multiplied by .25
        self.statmods_multipliers={-6:0.25,-5:0.38,-4:0.33,-3:0.4,-2:0.5,-1:0.66,0:1,\
                                   1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}
        #Set all changing values to their start values:
        self.reset()

    def take_damage(self,other,chosen_move, working_move, verbose = False):
        '''A function for a pokemon to take damage from a move. 
        Calls other pokemon and the move. Returns the damage'''
        level = other.level
        #Calculates threshold for a critical hit:
        if other.focus_energy:
            if working_move['effect'] == 'high critical hit ratio.':
                T = 4*(other.start_speed//4)
            else:
                T = other.start_speed//8
        else:
            if working_move['effect'] == 'high critical hit ratio.':
                T = 8*(other.start_speed//2)
            else:
                T = other.start_speed//2
        if T > 255: #threshold cannot exceed 255
            T = 255
        if random.randint(1,256) < T: #If hit is critical, set damage multiplier
            critical = (2*level+5)/(level+5)
        else:
            critical = 1

        if working_move['category'] == 'special':#for special move, use sp attack/defense
            A = other.sp_attack*self.statmods_multipliers[self.statmods['sp_attack']]
            D = self.sp_defense*self.statmods_multipliers[self.statmods['sp_defense']]
        elif working_move['category'] == 'physical':#for physical move, use attack/defense
            A = other.attack*self.statmods_multipliers[self.statmods['attack']]
            if other.effects_nv['burn']:
                A = A/2
            D = self.defense*self.statmods_multipliers[self.statmods['defense']]
        #if the move type matches the attacker's type: Same Type Attack Bonus
        if working_move['type'] in other.types: 
            STAB = 1.5 
        else:
            STAB = 1
        power = working_move['power']

        multiplier = self.damage_multiplier[working_move['type']] #type disadvantage
        Random = random.randint(217,255)/255

        Damage = (((((2*level*critical/5)+2)*power*A/D)/50)+2)*STAB*multiplier*Random

        self.hp = self.hp - Damage
        return Damage

    def confusion_damage(self,verbose = False):
        level =  self.level
        critical = 1
        power = 40
        STAB = 1
        A = self.attack*self.statmods_multipliers[self.statmods['attack']]
        D = self.defense*self.statmods_multipliers[self.statmods['defense']]
        if self.effects_nv['burn']:
                A = A/2
        Random = random.randint(217,255)/255
        multiplier = 1
        Damage = (((((2*level*critical/5)+2)*power*A/D)/50)+2)*STAB*multiplier*Random
        self.hp -= Damage
        verboseprint("%s hit itself in its confusion! %.2f damage! %.2f hp remaining." % \
                     (self.name, Damage, self.hp),verbose)
        

    def choose_move(self,other,verbose=False):
        '''Randomly choses a move from pokemon's available moveset.
        If pokemon doesn't have status effects preventing them to use move, apply use move.
        Apply poison or burn damage after'''
        #choose from available moves. If pokemon cannot use a move, removes from list
        available_moves = list(self.moveset.keys())
        if self.move_embargo in available_moves:
            available_moves.remove(self.move_embargo)

        #If there are still moves to choose from, randomly select a move
        if len(available_moves)>=1:
            chosen_move = random.choice(available_moves)
        else: chosen_move = "struggle"

        #Status effects that prevent moving:
        #Cannot move if asleep. Counts down to recover from sleep effects
        if self.effects_nv['sleep']:
            asleep = True
            self.effect_counter['sleep'] -=1
            if self.effect_counter['sleep'] == 0:
                self.effects_nv['sleep'] = False
        else:
            asleep = False

        #Cannot move if flinched (Lasts one move)
        if self.effects_v['flinch']:
            flinched = True
            self.effect_counter['flinch'] =0
            self.effects_v['flinch'] = False
        else:
            flinched = False

        #Paralysis has a 25 percent chance of making a pokemon unable to move
        if self.effects_nv['paralysis']:
            if random.random() < .25:
                fully_paralyzed = True
                self.frenzy = False
                self.effect_counter['frenzy'] = 0
                self.frenzy_move = False
            else: fully_paralyzed = False
        else:
            fully_paralyzed = False

        #Cannot move if frozen
        if self.effects_nv['freeze']:
            frozen = True
        else:
            frozen = False

        #cant_move boolean variable is True for any status effect that prevents moving
        cant_move = fully_paralyzed or asleep or frozen or flinched

        #Inflict confusion:
        if self.effects_v['confusion'] and not cant_move:
            if random.random() < .5:
                confused = True
                self.confusion_damage(verbose)
                self.frenzy = False
                self.effect_counter['frenzy'] = 0
                self.frenzy_move = False
                self.underground = False
                self.dig_move = False
            else:
                confused = False
            self.effect_counter['confusion'] -= 1
            if self.effect_counter['confusion'] ==0:
                self.effects_v['confusion'] = False
        else: confused = False

        #Effect of Petal Dance or thrash:
        if self.frenzy == True:
            chosen_move = self.frenzy_move
            if not cant_move:
                self.effect_counter['frenzy']-=1
            if self.effect_counter['frenzy'] == 0:
                self.frenzy_move = False
                self.frenzy = False
                self.effects_v['confusion'] = True

        cant_attack = cant_move or confused or self.underground

        #Effect of dig:
        if self.underground and not fully_paralyzed:
            chosen_move = self.dig_move
            self.use_move(other,chosen_move,verbose)
            self.underground = False
            

        #Effect of rage:
        if self.rage:
            chosen_move = self.rage_move

        if cant_move:
            verboseprint("  %s can't move." % (self.name),verbose)
        #If pokemon can move and there is an available move they can use:
        if (not cant_attack) and (chosen_move):
            self.use_move(other,chosen_move,verbose) #use move

        #Inflict poison or burn damage
        if self.effects_nv['poison'] or self.effects_nv['burn']:
            damage = self.start_hp//16
            if damage == 0:
                damage = 1
            self.hp -= damage
            verboseprint("  %s took %d poison/burn damage" % (self.name,damage),verbose)

        #Inflict Seeding
        if self.effects_v['seed']:
            damage = self.start_hp//16
            if damage == 0:
                damage = 1
            self.hp -= damage
            newhp = other.hp + damage
            if newhp > other.start_hp:
                other.hp = other.start_hp
            verboseprint("  %s took %d seeding damage" % (self.name,damage),verbose)
            verboseprint("  %s gains %d hp!" % (other.name,damage),verbose)

    def use_move(self,other,chosen_move,verbose=False):
        '''Use a chosen move against another pokemon'''

        verboseprint("%s used %s!" % (self.name,chosen_move),verbose)

        #use_move can be called with a move that is not in the Pokemon's individual moveset.
        #if so, recreates a move dictionary for that specific move
        if chosen_move in self.moveset:
            working_move = self.moveset[chosen_move]
        else:
            move = merged_moves_df.iloc[np.where(merged_moves_df['move'] == \
                                                 chosen_move)].iloc[0]
            working_move = {'type':move['type'],\
                             'power':move['power'],\
                             'accuracy':move['accuracy'],\
                             'pp':move['pp'],\
                             'category':move['category'],\
                             'effect':move['effect'],\
                             'effect_prob':move['effect_prob']/100}

        #if no other move has been used yet, assign as first move
        if not self.first_move:
            self.first_move = working_move
            
        #Accuracy:
        # if accuracy is inapplicable, move always works.
        if working_move['accuracy'] == '_':
                acc = 1
        else: #convert accuracy to a probability
            #Accuracy depends on individual accuracy, move accuracy, and other's evasion
            move_acc = float(working_move['accuracy'])
            self_acc = self.statmods_multipliers[self.statmods['accuracy']]
            other_evasion = other.statmods_multipliers[other.statmods['evasion']]
            acc = move_acc*self_acc*(1/other_evasion)/100
         

        ####
        #if the other pokemon is underground they are immune to most moves
        #(not swift or transform)
        if other.underground and (chosen_move != 'swift') and (chosen_move != 'transform'):
            acc = 0
        
        #Given the accuracy, does the move hit?
        if random.random() < acc: #bernoulli with p = acc on whether move hits or not
            verboseprint("%s's move hits!" % (self.name),verbose) #display whether move hits
            #If the move has effect, take effect
            if (working_move['effect'] is not np.nan):
                self.take_effect(other,chosen_move,working_move,verbose)
            #if the move hits and it's special or physical, the other pokemon takes damage
            if (working_move['category'] == 'special') or \
            (working_move['category'] == 'physical'):
                if not self.underground:
                    dam = other.take_damage(self,chosen_move, working_move, verbose)
                    if other.rage:
                      other.take_status('attack',1)
                
                # for life stealing moves:
                if (working_move['effect'] == \
                    "user recovers half the hp inflicted on opponent."):
                    self.hp += dam/2
                    if self.hp > self.start_hp:
                        self.hp = self.start_hp
                #for recoil damage
                if (working_move['effect'] == 'user receives recoil damage.'):
                    self.hp -= dam/4
                if chosen_move == "struggle":
                    self.hp -= dam/2
                if (working_move['effect'] == 'always inflicts 40 hp.'):
                    dam = (40-dam)
                    other.hp -= dam
                    dam = 40  #for print statement
                if (working_move['effect'] == 'always inflicts 20 hp.'):
                    dam = (20-dam)
                    other.hp -= dam
                    dam = 20 #for print statement

                #print out damage
                if not self.underground:
                    verboseprint("  %s hit for %.2f damage!" % (chosen_move, dam),verbose)

            #status moves don't have damage outside of their effects
            elif working_move['category'] == 'status':
                if chosen_move == "transform":
                    self.transform(other)

        else: # display whether move misses
            verboseprint("%s's move misses..." % (self.name),verbose) 
        #Saves the move as last_attack
        self.last_attack = chosen_move

    def take_effect(self,other,chosen_move,working_move,verbose=False):
        '''Applies move affects to the appropriate pokemon
        takes as arguments other, the move name, move dictionary, and verbose'''

        effect = working_move['effect'] #Assigns effect to a variable
        verboseprint(f'  {effect}',verbose) #Print the effect if verbose is true

        ## Modifies other's stats
        if effect == "lowers opponent's attack.":
            other.take_status('attack',-1)
        if effect == "lowers opponent's defense.":
            other.take_status('defense',-1)
        if effect == "sharply lowers opponent's defense.":
            other.take_status('defense',-2)
        if effect == "sharply lowers opponent's speed.":
            other.take_status('speed',-2)
        if effect == "lowers opponent's accuracy.":
            other.take_status('accuracy',-1)
        if effect == "may lower opponent's special defense.":
            if random.random() < working_move['effect_prob']:
                other.take_status('sp_defense',-1)
        if (effect == "may lower opponent's speed.") or \
        (effect == "may lower opponent's speed by one stage."):
            if random.random() < working_move['effect_prob']:
                other.take_status('speed',-1)
        if effect == "may lower opponent's attack.":
            if random.random() < working_move['effect_prob']:
                other.take_status('attack',-1)

        #Modifies Own Stats:
        if effect == "raises user's defense.":
            self.take_status('defense',1)
        if effect == "sharply raises user's defense.":
            self.take_status('defense',2)
        if effect == "sharply raises user's special defense.":
            self.take_status('sp_defense',2)
        if effect == "raises user's attack and special attack.":
            self.take_status('attack',1)
            self.take_status('sp_attack',1)
        if effect == "raises user's attack.":
            self.take_status('attack',1)
        if effect == "sharply raises user's speed.":
            self.take_status('speed',2)
        if effect == "sharply raises user's evasiveness.":
            self.take_status('evasion',2)
        if effect == "raises user's attack when hit.":
            self.rage = True
            self.rage_move = chosen_move

        #Check other's statuses: (returns true if they already have a status effect)
        nv_effects = other.check_effects()

        #Changes statuses that don't have multipliers:
        if not nv_effects: #Non-volatile statuses don't get overwritten
            if effect == "puts opponent to sleep.":
                other.effects_nv['sleep'] = True
                other.effect_counter['sleep'] = random.randint(1,7)
            if (effect =='poisons opponent.') and ('poison' not in other.types):
                other.effects_nv['poison']=True
            if (effect == 'may poison the opponent.') or (effect =='may poison opponent.'):
                if (random.random() < working_move['effect_prob']) \
                and ('poison' not in other.types.values()):
                    other.effects_nv['poison']=True
            if (effect == 'paralyzes opponent.') \
            and (working_move['type'] not in other.types.values()):
                other.effects_nv['paralysis']= True
            if (effect == 'may paralyze opponent.') \
            and (working_move['type'] not in other.types.values()):
                if (random.random() < working_move['effect_prob']):
                    other.effects_nv['paralysis']= True
            if effect == 'may freeze opponent.':
                if 'ice' not in other.types.values():
                    if random.random() < working_move['effect_prob']:
                        other.effects_nv['freeze'] = True
        #Burn counteracts freezing and is the exception to a non-volatile statuses staying
        if (not nv_effects) or (other.effects_nv['freeze']):
            if effect == 'may burn opponent.':
                other.effects_nv['freeze'] = False
                if (random.random() < working_move['effect_prob']) \
                and ('fire' not in other.types.values()):
                    other.effects_nv['burn'] = True

        #Volatile Status effects:
        if effect == 'confuses opponent.':
            other.effects_v['confusion'] = True
            other.effect_counter['confusion'] = random.randint(1,3)
        if effect == 'may confuse opponent.':
            if random.random() < working_move['effect_prob']:
                other.effects_v['confusion'] = True
                other.effect_counter['confusion'] = random.randint(1,3)
        if effect == 'may cause flinching.':
            if random.random() < working_move['effect_prob']:
                other.effects_v['flinch'] = True
                other.effect_counter['flinch'] = 1
        if (effect == 'drains hp from opponent each turn.') \
        and ('grass' not in other.types.values()):
            other.effects_v['seed']= True

        #Special effects
        if effect == "inflicts damage equal to user's level.":
            other.hp -= self.level
        if effect == 'increases critical hit ratio.':
            self.focus_energy = True
        if effect == 'hits 2-5 times in one turn.':
            ntimes = random.randint(1,4)
            for i in range(ntimes):
                other.take_damage(self,chosen_move, working_move, verbose)
        if effect == 'hits twice in one turn.':
            other.take_damage(self,chosen_move, working_move, verbose)
        if effect ==  'user attacks for 2-3 turns but then becomes confused.':
            self.frenzy = True
            self.effect_counter['frenzy'] = random.randint(2,3)
            self.frenzy_move = chosen_move
        if (not self.underground) and (effect == 'digs underground on first turn, attacks on second. can also escape from caves.'):
            verboseprint('  user digs underground',verbose)
            self.underground = True
            self.dig_move = chosen_move
        elif self.underground and (effect == 'digs underground on first turn, attacks on second. can also escape from caves.'):
            verboseprint('  user strikes from below',verbose)
            self.underground = False
        if effect == "changes user's type to that of its first move.":
            if self.first_move != working_move:
                self.types[1] = self.first_move['type']
        if effect == 'user performs almost any move in the game at random.':
            available_moves = list(merged_moves_df.move.unique())
            chosen_move = random.choice(available_moves)
            self.use_move(other,chosen_move,verbose)
        if (effect == 'in battles, the opponent switches. in the wild, the pokémon runs.')\
         or (effect =='allows user to flee wild battles; also warps player to last pokécenter.'):
            self.in_battle = False
            verboseprint('  teleported away',verbose)
        if effect == "opponent can't use its last attack for a few turns.":
            other.move_embargo = other.last_attack
            other.effect_counter['move_embargo'] = 2
        if effect == 'user sleeps for 2 turns, but user is fully healed.':
            self.effects_nv['sleep'] = True
            self.effect_counter['sleep'] = 2
            self.rest = True
            self.hp = self.start_hp
            self.effects_nv['poison']=False
            self.effects_nv['paralysis']=False
            self.effects_nv['burn'] = False
            self.effects_nv['freeze'] = False


        # Added verbose statements for effect changes
        # filter by effects that are true using a filter function
        if True in self.effects_nv.values():
            active_nv_effects = list(filter(lambda key: self.effects_nv[key],\
                                            self.effects_nv.keys()))
            verboseprint(f'  {self.name} has status: {active_nv_effects}',verbose)
        if True in self.effects_v.values():
            active_v_effects = list(filter(lambda key: self.effects_v[key],\
                                           self.effects_v.keys()))
            verboseprint(f'  {self.name} has status: {active_v_effects}',verbose)

        if True in other.effects_nv.values():
            active_nv_effects = list(filter(lambda key: other.effects_nv[key],\
                                            other.effects_nv.keys()))
            verboseprint(f'  {other.name} has status: {active_nv_effects}',verbose)
        if True in other.effects_v.values():
            active_v_effects = list(filter(lambda key: other.effects_v[key],\
                                           other.effects_v.keys()))
            verboseprint(f'  {other.name} has status: {active_v_effects}',verbose)


    def take_status(self,status_name,modification):
        '''Adjusts the stage of a stat to change its multipliers.'''
        new_status = self.statmods[status_name] + modification
        #Stage must be between -6 and 6
        if new_status < -6:
            self.statmods[status_name] = -6
        elif new_status > 6:
            self.statmods[status_name] = 6
        else:
            self.statmods[status_name] = new_status

    def check_effects(self):
        '''returns True if there is a nonvolatile status in place'''
        nv_effects = False
        for status in self.effects_nv:
            nv_effects = nv_effects or self.effects_nv[status]
        return nv_effects

    def transform(self,other):
        '''Status move where pokemon takes traits of the other pokemon'''
        self.speed = other.speed
        self.types = other.types
        self.moveset = other.moveset
        self.damage_multiplier = other.damage_multiplier
        self.attack = other.attack
        self.defense = other.defense
        self.sp_attack = other.sp_attack
        self.sp_defense = other.sp_defense

    def healthpercent(self):
        return round(self.hp/self.start_hp,3)

    def reset(self):
        '''Resets all conditions to starting conditions'''
        #Base stats, type, and modifiers:
        self.hp = self.start_hp
        self.speed = self.start_speed
        self.defense = self.start_defense
        self.attack = self.start_attack
        self.sp_attack = self.start_sp_attack
        self.sp_defense = self.start_sp_defense
        self.types = self.start_types
        self.damage_multiplier = self.start_damage_multiplier
        self.statmods = {'speed':0,'attack':0,'defense':0,'sp_attack':0,\
                         'sp_defense':0,'accuracy':0,'evasion':0}
        self.moveset = self.start_moveset
        #nonvolatile status effects:
        self.effects_nv = {'sleep':False,'paralysis':False,'poison':False,\
                           'freeze':False,'burn':False}
        #volatile status effects:
        self.effects_v = {'confusion':False,'flinch':False,'seed':False,}
        #Statuses to keep track of states
        self.effect_counter = {'sleep':0,'confusion':0,'poison':0,\
                               'move_embargo':0,'flinch':0,'frenzy':0}
        self.first_move = False
        self.last_attack = False
        self.move_embargo = False
        self.in_battle = True
        self.focus_energy = False
        self.frenzy = False
        self.frenzy_move = False
        self.underground = False
        self.dig_move = False
        self.rage = False
        self.rage_move = False
        self.rest = False

#-------------------------------------------------------------------------------------
## Run Battle
def runbattle(pokemon_a,pokemon_b,verbose=False,healing=False,remaininghealth = 1,freshstart=True):
    '''pokemon_a and pokemon_b: Pokemon class
    verbose: boolean, print or don't print moves 
    healing: boolean for whether to heal in battle
    remaininghealth: percent of health pokemon b has left (between 0 and 1)
    freshstart: boolean for whether to reset at the beginning of a match '''
    #check if pokemon a is the same as pokemon b
    if pokemon_a.name == pokemon_b.name:
        #create a copy of pokemon b with a different name
        pokemon_b = copy.deepcopy(pokemon_a)
        pokemon_b.name = pokemon_b.name + '2'

    #reset the stats of both pokemon
    if freshstart:
        pokemon_a.reset()
        pokemon_b.reset()

    #if healing is True, set a number of heals per battle
    if healing:
        Nheals1 = 1
        Nheals2 = 1
    else:
        Nheals1 = 0
        Nheals2 = 0
    healingthreshold = 0.15 #heals at 15 percent of original health

    pokemon_b.hp = pokemon_b.start_hp*(remaininghealth)
    verboseprint("->%s has %.1f hp.\n->%s has %.1f hp." % (pokemon_a.name,pokemon_a.hp,pokemon_b.name,pokemon_b.hp),verbose)

    #fastest pokemon is "pokemon1", who goes first
    if pokemon_a.start_speed > pokemon_b.start_speed:
        pokemon1=pokemon_a
        pokemon2=pokemon_b
    elif pokemon_b.start_speed > pokemon_a.start_speed:
        pokemon1=pokemon_b
        pokemon2=pokemon_a
    else: #for pokemon with the same speed, randomly select who goes first
        if random.random() < 0.5:
            pokemon1 = pokemon_a
            pokemon2 = pokemon_b
        else:
            pokemon1 = pokemon_b
            pokemon2 = pokemon_a

    verboseprint("%s goes first!" % pokemon1.name,verbose)
    nturns = 0

    while pokemon1.hp >0 and pokemon2.hp>0:
        
        #Pokemon 1: heals or takes a turn
        if (Nheals1 > 0) and (pokemon1.hp < healingthreshold * pokemon1.start_hp):
            Nheals1 -= 1
            pokemon1.reset()
            verboseprint("%s used a full restore!" % pokemon1.name,verbose)
        else:
            pokemon1.choose_move(pokemon2,verbose)
        verboseprint("-- %s has %.1f hp remaining." % (pokemon2.name,pokemon2.hp),verbose)
        nturns += 1
        
        #Check for a winner 
        winner = check_winner(pokemon1,pokemon2)
        if winner: 
            if winner != 'draw':
                verboseprint('\n%s wins after %d turns! %d percent of health remaining\n' % (winner.name,nturns,winner.healthpercent()*100),verbose)
                return winner.name, nturns, pokemon_a.healthpercent(),pokemon_b.healthpercent()
            else:
                return winner,nturns,pokemon_a.healthpercent(),pokemon_b.healthpercent()
        if pokemon1.in_battle == False:
            verboseprint('\n%s left the battle, draw after %d turns' % (pokemon1.name, nturns), verbose)
            return 'draw', nturns, pokemon_a.healthpercent(),pokemon_b.healthpercent()
        #Pokemon 2: heals or takes a turn
        if (Nheals2 > 0) and (pokemon2.hp < healingthreshold * pokemon2.start_hp):
            Nheals2 -= 1
            pokemon2.reset()
            verboseprint("%s used a full restore!" % pokemon2.name,verbose)
        else:
            pokemon2.choose_move(pokemon1,verbose)
        verboseprint("-- %s has %.1f hp remaining." % (pokemon1.name,pokemon1.hp),verbose)
        nturns +=1

        #Check for a winner
        winner = check_winner(pokemon1,pokemon2)
        if winner:
            #healthperc = winner.hp/winner.start_hp
            if winner != 'draw':
                verboseprint('\n%s wins after %d turns! %d percent of health remaining\n' % (winner.name,nturns,winner.healthpercent()*100),verbose)
                return winner.name, nturns, pokemon_a.healthpercent(),pokemon_b.healthpercent()
            else:
                return 'draw',nturns,pokemon_a.healthpercent(),pokemon_b.healthpercent()
        # Check if pokemon 2 has left the battle    
        if pokemon2.in_battle == False:
            verboseprint('\n%s left the battle, draw after %d turns' % (pokemon2.name, nturns), verbose)
            return 'draw', nturns, pokemon_a.healthpercent(),pokemon_b.healthpercent()
        # Check if the battle has gone on for too long
        if nturns >100:
            verboseprint('\ndraw after %d turns' % nturns, verbose)
            return 'draw', nturns, pokemon_a.healthpercent(),pokemon_b.healthpercent()

#----------------------------------------------------------------------------------------

def check_winner(pokemona,pokemonb):
    '''Returns winner's name if either pokemon's hp has decreased below zero'''
    if pokemona.hp <=0 and pokemonb.hp<=0:
        pokemona.hp = 0
        pokemonb.hp = 0
        return 'draw'
    elif pokemona.hp <=0:
        pokemona.hp = 0
        return pokemonb
    elif pokemonb.hp <=0:
        pokemonb.hp = 0
        return pokemona
    else:
        return False
    
#----------------------------------------------------------------------------------------

def create_pokemon_dict(generation = 1):
    '''Create a dictionary of pokemon objects'''
    # Assign all pokemon as a class
    gen1 = np.where(Pokemon_df['generation'] == generation) #isolates gen 1 pokemon
    pokemon_dict = {} #Dictionary in {Pokemon name:Pokemon class format}
    for pokemon_name in Pokemon_df.iloc[gen1].index: #for every pokemon in gen 1
        #assign a class as a member of the dictionary
        pokemon_dict[pokemon_name] = Pokemon(pokemon_name)
    return pokemon_dict

#----------------------------------------------------------------------------------------

def battle_team(team_1, team_2, verbose=False,roundreset = True):
    '''Runs a battle between two teams of pokemon. Returns the winner 
    winner list, and the number of rounds it took to win.'''
    team_1_names = [pokemon.name for pokemon in team_1]
    team_2_names = [pokemon.name for pokemon in team_2]
    # reset all pokemon
    if roundreset:
        for pokemon in team_1:
            pokemon.reset()
        for pokemon in team_2:
            pokemon.reset()
    rounds = 0
    winner_list = []
    n = 0
    percent_health_a = 1
    
    for opponent in team_2:
        percent_health_b = 1
        for i in range(n,len(team_1)):
            if percent_health_b > 0:
                if percent_health_a == 1:
                    winner, round_count, percent_health_a, percent_health_b = runbattle(team_1[i], opponent, verbose = verbose, healing=False, remaininghealth = percent_health_b)
                    winner_list.append(winner)
                    rounds += round_count
                else:
                    winner, round_count, percent_health_b, percent_health_a = runbattle(opponent, team_1[i], verbose = verbose, healing=False, remaininghealth = percent_health_a)
                    winner_list.append(winner)
                    rounds += round_count
                if percent_health_a <= 0:
                    n += 1
                    percent_health_a = 1
            else:
                break
    if winner_list[-1] in team_1_names:
        winner = '1st team'    
    else:
        winner = '2nd team'
    return winner, winner_list, rounds

def run_elite(our_team,elite4,verbose = False,roundreset = True):
    ''' Function to run the elite four battles. Input is a list of 6 pokemon and 
        the elite4 - these have to be pokemon objects.
        Returns a tuple of success,round_time,teamname,winner_list:
            Success is 1 if the team wins, 0 if the team loses.
            round_time is the number of rounds it took to win divided by 10. 
            Teamname is the name of the elite four member that the team lost to.
            Winner_list is a list of the winners from the final battle.
    '''
    success = 0
    winner = 'NA'
    round_time = 0
    teamname = 'NA'
    
    for team in elite4:
        if team ==  elite4[0]:
            winner,winner_list,rounds = battle_team(our_team,team,verbose,True)
        else:
            winner,winner_list,rounds = battle_team(our_team,team,verbose,roundreset)
        round_time += rounds
        if winner == "2nd team":
            if team == elite4[0]:
                teamname = 'Lorelei'
            elif team == elite4[1]:
                teamname = 'Bruno'
            elif team == elite4[2]:
                teamname = 'Agatha'
            elif team == elite4[3]:
                teamname = 'Lance'
            else:
                teamname = 'Error: Team not found'
            round_time = round_time/10
            return success,round_time,teamname,winner_list
    round_time = round_time/10
    teamname = 'Champion'
    success = 1
    return success,round_time,teamname,winner_list

if __name__ == '__main__':
    #----------------------------------------------------------------------------------------
    # Test Battle
    #----------------------------------------------------------------------------------------
    # Create a dictionary of pokemon objects
    pokemon_dict = create_pokemon_dict()
    # Enter Pokemon one
    pokemon1 = 'charizard'
    # Enter Pokemon two
    pokemon2 = 'blastoise'
    # Run the battle
    runbattle(pokemon_dict[pokemon1],pokemon_dict[pokemon2],verbose=True)