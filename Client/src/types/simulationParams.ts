interface SimulationParams {
    number_of_people?: number;
    number_of_floors?: number;
    choice_mode?: number;
    time_for_firefighters?: number;
    fire_spread_rate?: number;
    max_visibility?: number;
    min_visibility?: number;
    max_strength?: number;
    min_strength?: number;
    max_speed?: number;
    min_speed?: number;
    max_fear?: number;
    min_fear?: number;
    max_age?: number;
    min_age?: number;
    max_health?: number;
    min_health?: number;
    likes_people_probability?: number;
    familiarity?: number;
    copycat?: number;
    cooperator?: number;
    detective?: number;
    simpleton?: number;
    cheater?: number;
    grudger?: number;
    copykitten?: number;
    random?: number;
}

export default SimulationParams;