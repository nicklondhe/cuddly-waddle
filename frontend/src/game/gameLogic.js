export const shuffleArray = (array) => {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
  };
  
  export const checkGuess = (selectedMovies) => {
    if (selectedMovies.length !== 4) {
      return {
        isCorrect: false,
        message: 'Select exactly 4 movies'
      };
    }
  
    const groupIds = new Set(selectedMovies.map(movie => movie.group_id));
    
    if (groupIds.size === 1) {
      return {
        isCorrect: true,
        groupId: selectedMovies[0].group_id
      };
    }
  
    // Check if "off by one"
    const groupCounts = selectedMovies.reduce((acc, movie) => {
      acc[movie.group_id] = (acc[movie.group_id] || 0) + 1;
      return acc;
    }, {});
  
    const maxInSameGroup = Math.max(...Object.values(groupCounts));
    return {
      isCorrect: false,
      message: maxInSameGroup === 3 ? 'Almost there! One movie away from a group' : 'Try again!'
    };
  };
  
  export const getGroupTheme = (groups, groupId) => {
    const group = groups.find(g => g.id === groupId);
    return group ? group.theme : '';
  };
  
  export const initializeGameState = (items) => {
    return shuffleArray(items).map(item => ({
      ...item,
      isSelected: false,
      isCompleted: false
    }));
  };
  
  export const colorSchemes = ['teal', 'purple', 'blue', 'cyan'];