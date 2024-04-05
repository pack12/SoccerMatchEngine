import numpy as np
class playerActionOffBall:
    def __init__(self,playerData, zoneData,ball):

        """Check to see if a player has ball"""
        if playerData.get_player_with_ball() == None:

            #emptyZonePassRates = playerData.findEmptyZonePassRates(zoneData)  # Will be in form of {<zoneObject>: 0.80}

            """Need to find the ball"""
            ballZone = zoneData.zoneInfo[ball.currentIndex - 1]

            """Need to get players close to the ball"""
            zoneIndexes = []
            surroundingTargetZones = []
            players_surrounding_ball = []

            if ballZone.index != 67 and ballZone.index != 68:
                nZoneIndex = ballZone.index - 11
                zoneIndexes.append(nZoneIndex)
                neZoneIndex = ballZone.index - 10
                zoneIndexes.append(neZoneIndex)
                nwZoneIndex = ballZone.index - 12
                zoneIndexes.append(nwZoneIndex)
                wZoneIndex = ballZone.index - 1
                zoneIndexes.append(wZoneIndex)
                eZoneIndex = ballZone.index + 1
                zoneIndexes.append(eZoneIndex)
                sZoneIndex = ballZone.index + 11
                zoneIndexes.append(sZoneIndex)
                swZoneIndex = ballZone.index + 10
                zoneIndexes.append(swZoneIndex)
                seZoneIndex = ballZone.index + 12
                zoneIndexes.append(seZoneIndex)
            for i in zoneIndexes:
                # Get the Zone
                if i > 0 and i < 67:

                    zone = zoneData.zoneInfo[i - 1]
                    surroundingTargetZones.append(zone)
                    if ballZone.rightEdge == True and zone.leftEdge == True:
                        # Don't add this zone as an available zone
                        surroundingTargetZones.remove(zone)
                    elif ballZone.leftEdge == True and zone.rightEdge == True:
                        surroundingTargetZones.remove(zone)
            print(f'Printing players around ball')
            for zone in surroundingTargetZones:
                # print(zone.attached_players)
                for team_name in zone.attached_players:
                    #Players go to ball for now
                    # print(team_name)
                    # print(zone.attached_players[team_name])
                    for player in zone.attached_players[team_name]:

                        playerZone = zoneData.zoneInfo[player.Index - 1]
                        futureZone = zoneData.zoneInfo[ballZone.index - 1]
                        players_surrounding_ball.append(player)
                        print(f'Adding {player} to surrounding_ball lsit!')
                        #This is for when we want to actually move the players

            #Sort players by speed
            sorted_list = sorted(players_surrounding_ball, key=lambda player: player.speed)  # sort by age
            print(players_surrounding_ball)
            for i in range(len(sorted_list)):
                print(f'Name: {sorted_list[i].fullName} Speed: {sorted_list[i].speed}')
                speed = sorted_list[i].speed
                workRate = sorted_list[i].workRate
                distance = playerData.findDistanceToBall(zoneData,sorted_list[i],ball) #Temporary, create a function that finds distance between player and ball
                denominator = 1 + np.exp((-0.1 * speed) - (0.01 * workRate) + (0.1 * distance))

                # print(denominator)
                rate = 1 / denominator
                print(rate)

                print(f'Based on distance / speed: time={distance/speed}')
                """
                for k in playerZone.Locations:
                    if playerZone.Locations[k][1] == player:
                        playerZone.Locations[k].remove(player)
                        playerZone.Locations[k].append(None)
                        playerZone.attached_players[player.Team].remove(player)


                player_rect_from_dict = playerData.playerRects[player]
                print(f'PlayerIndex before Del: {player.Index}')
                del playerData.playerRects[player]
                # playerWithBall.Index = futureZoneIndex        #Originally, this is how I moved players before changing player.move function
                player.move(ballZone.index)
                playerData.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)
                print('Index should be updated!')
                print(f'PlayerWithBallIndex: {player.Index}') """


        else:
            print('why this')
            for i in playerData.playerRects:
                print(i)
