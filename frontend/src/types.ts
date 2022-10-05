export interface Player {
    name: string;
    points: number;
    games: Game[];
}

export interface Game {
    id: string;
    rounds: Score[];
    map_name: string;
    points: number;
    date: string;
}

export interface Score {
    id: number;
    round: object[];

    round_id: number;
    player_id: number;
    lat: number;
    lng: number;
    timed_out: boolean;
    timed_out_with_guess: boolean;
    round_score_points: number;
    round_score_percentage: number;
    distance_meters: number;
    time: number
}
