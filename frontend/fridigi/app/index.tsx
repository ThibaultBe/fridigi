import React from 'react';
import { View, Text, StyleSheet, Pressable, FlatList } from 'react-native';
import { Link, router } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { BlurView } from 'expo-blur';

export default function HomeScreen() {
  const data = [
    { id: '1', title: 'Fridge-tuscany', sharedBy: 'Shared by Alex, Thibault and Max'},
    //{ id: '2', title: '' },
    //{ id: '3', title: 'Third Item' },
  ];
  
  const renderItem = ({ item }) => (
    <Pressable 
      style={({ pressed }) => [
        styles.blueBox,  // This is the key - we need to use the blue box style
        pressed && styles.blueBoxPressed
      ]}
      onPress={() => {
        console.log(`Pressed ${item.title}`);
        router.push("/fridge")
      }}
    >
      
      <View style={styles.fridgeTextContainer}>
        <Text style={styles.fridgeTitle}>{item.title}</Text>
        {item.sharedBy && <Text style={styles.fridgeSharedBy}>{item.sharedBy}</Text>}
      </View>
      <Text style={styles.fridgeIcon}>🐟</Text> 
    </Pressable>
  );

  return (
    <View style={styles.container}>
      
      <View style={styles.listContainer}>
        <FlatList
          data={data}
          renderItem={renderItem}
          keyExtractor={item => item.id}
          style={styles.list}
          contentContainerStyle={styles.listContent}
        />
      </View>
      
      <StatusBar style='dark'/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#DBF0FA',
    padding: 20,
    paddingTop: 50,
  },
  headerTitle: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#003366',
    marginBottom: 15,
  },
  listContainer: {
    width: '100%',
    flex: 1,
  },
  list: {
    width: '100%',
  },
  listContent: {
    paddingBottom: 20,
  },
  // This is the blue box style that was missing
  blueBox: {
    backgroundColor: '#007AFF',
    padding: 15,
    marginVertical: 8,
    borderRadius: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    // Shadow for iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    // Elevation for Android
    elevation: 2,
  },
  blueBoxPressed: {
    opacity: 0.8,
    backgroundColor: '#0069d9',
  },
  fridgeTextContainer: {
    flex: 1,
  },
  fridgeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  fridgeSharedBy: {
    fontSize: 12,
    color: 'white',
    opacity: 0.9,
    marginTop: 4,
  },
  fridgeIcon: {
    fontSize: 18,
    marginLeft: 10,
    color: 'white',
  }
});