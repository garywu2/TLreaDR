import {
  FETCH_CATEGORIES,
  ADD_CATEGORY,
  DELETE_CATEGORY
} from "../actions/types";

const categoriesReducer = (state = null, action) => {
  switch (action.type) {
    case FETCH_CATEGORIES:
      return action.categories;
    case ADD_CATEGORY:
      return [...state, action.category];
    case DELETE_CATEGORY:
      return state.filter(category => category.name !== action.categoryName);
    default:
      return state;
  }
};

export default categoriesReducer;
