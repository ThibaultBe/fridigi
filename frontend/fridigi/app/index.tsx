import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { Link, router } from 'expo-router';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to My App</Text>
      
      {/* Option 1: Using the Link component */}
      <Link href="/fridge" asChild>
        <Pressable style={styles.button}>
          <Text style={styles.buttonText}>Go to Fridge (Link)</Text>
        </Pressable>
      </Link>
      
      {/* Option 2: Using the router.push method */}
      <Pressable 
        style={[styles.button, styles.buttonAlt]} 
        onPress={() => router.push('/fridge')}
      >
        <Text style={styles.buttonText}>Go to Fridge (router.push)</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 8,
    marginVertical: 10,
    width: '80%',
    alignItems: 'center',
  },
  buttonAlt: {
    backgroundColor: '#5856D6',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
