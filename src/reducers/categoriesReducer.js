import { FETCH_CATEGORIES } from '../actions/types';

const categoriesReducer = (state = null, action) => {
    switch (action.type) {
        case FETCH_CATEGORIES:
            return action.categories;
        default:
            return state;
    }
};

export default categoriesReducer;