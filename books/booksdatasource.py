#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 18 September 2018

    For use in some assignments at the beginning of Carleton's
    CS 257 Software Design class, Fall 2018.
'''
import datetime
import csv
import sys


class BooksDataSource:
    '''
    A BooksDataSource object provides access to data about books and authors.
    The particular form in which the books and authors are stored will
    depend on the context (i.e. on the particular assignment you're
    working on at the time).

    Most of this class's methods return Python lists, dictionaries, or
    strings representing books, authors, and related information.

    An author is represented as a dictionary with the keys
    'id', 'last_name', 'first_name', 'birth_year', and 'death_year'.
    For example, Jane Austen would be represented like this
    (assuming her database-internal ID number is 72):

        {'id': 72, 'last_name': 'Austen', 'first_name': 'Jane',
         'birth_year': 1775, 'death_year': 1817}

    For a living author, the death_year is represented in the author's
    Python dictionary as None.

        {'id': 77, 'last_name': 'Murakami', 'first_name': 'Haruki',
         'birth_year': 1949, 'death_year': None}

    Note that this is a simple-minded representation of a person in
    several ways. For example, how do you represent the birth year
    of Sophocles? What is the last name of Gabriel García Márquez?
    Should we refer to the author of "Tom Sawyer" as Samuel Clemens or
    Mark Twain? Are Voltaire and Molière first names or last names? etc.

    A book is represented as a dictionary with the keys 'id', 'title',
    and 'publication_year'. For example, "Pride and Prejudice"
    (assuming an ID of 132) would look like this:

        {'id': 193, 'title': 'A Wild Sheep Chase', 'publication_year': 1982}

    '''

    def __init__(self, books_filename, authors_filename, books_authors_link_filename):
        ''' Initializes this data source from the three specified  CSV files, whose
            CSV fields are:

                books: ID,title,publication-year
                  e.g. 6,Good Omens,1990
                       41,Middlemarch,1871


                authors: ID,last-name,first-name,birth-year,death-year
                  e.g. 5,Gaiman,Neil,1960,NULL
                       6,Pratchett,Terry,1948,2015
                       22,Eliot,George,1819,1880

                link between books and authors: book_id,author_id
                  e.g. 41,22
                       6,5
                       6,6

                  [that is, book 41 was written by author 22, while book 6
                    was written by both author 5 and author 6]

            Note that NULL is used to represent a non-existent (or rather, future and
            unknown) year in the cases of living authors.

            NOTE TO STUDENTS: I have not specified how you will store the books/authors
            data in a BooksDataSource object. That will be up to you, in Phase 3.
        '''
        self.bookList = []
        self.authorList = []
        self.link = []
        self.now = datetime.datetime.now()

        with open(books_filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] != 'NULL' and row[2] != '' :
                    book = {'id': int(row[0]), 'title': row[1], 'publication_year': int(row[2])}
                    self.bookList.append(book)

        with open(authors_filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[4] != 'NULL':
                    author = {'id': int(row[0]), 'last_name': row[1], 'first_name': row[2],
                     'birth_year': int(row[3]), 'death_year': int(row[4])}
                    self.authorList.append(author)
                else :
                    author = {'id': int(row[0]), 'last_name': row[1], 'first_name': row[2],
                     'birth_year': int(row[3]), 'death_year': None}
                    self.authorList.append(author)

        with open(books_authors_link_filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.link.append({'book_id' : int(row[0]), 'author_id' :  int(row[1])})

    def book(self, book_id):
        ''' Returns the book with the specified ID. (See the BooksDataSource comment
            for a description of how a book is represented.)

            Raises ValueError if book_id is not a valid book ID.
        '''
        for item in self.bookList:
            if item['id'] == book_id:
                return item
        return("Book not found")

    def books(self, *, author_id=None, search_text=None, start_year=None, end_year=None, sort_by='title'):
        ''' Returns a list of all the books in this data source matching all of
            the specified non-None criteria.

                author_id - only returns books by the specified author
                search_text - only returns books whose titles contain (case-insensitively) the search text
                start_year - only returns books published during or after this year
                end_year - only returns books published during or before this year

            Note that parameters with value None do not affect the list of books returned.
            Thus, for example, calling books() with no parameters will return JSON for
            a list of all the books in the data source.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                default -- sorts by (case-insensitive) title, breaking ties with publication_year

            See the BooksDataSource comment for a description of how a book is represented.

            QUESTION: Should Python interfaces specify TypeError?
            Raises TypeError if author_id, start_year, or end_year is non-None but not an integer.
            Raises TypeError if search_text or sort_by is non-None, but not a string.

            QUESTION: How about ValueError? And if so, for which parameters?
            Raises ValueError if author_id is non-None but is not a valid author ID.
        '''

        results_author_id = []
        results_search_text = []
        results_start_year = []
        results_end_year = []

        resultArray = [] # Maintains an array of array of results per speficiation

        if author_id != None:
            for id in self.link:
                if id['author_id']==author_id:
                    for book in self.bookList:
                        if book['id'] == id['book_id']:
                            results_author_id.append(book)
            resultArray.append(results_author_id)

        if search_text != None:
            for book in self.bookList:
                if book['title'].lower().find(search_text.lower())>-1:
                    results_search_text.append(book)
            resultArray.append(results_search_text)

        if start_year != None:
            for book in self.bookList:
                if book['publication_year']>= start_year:
                    results_start_year.append(book)
            resultArray.append(results_start_year)

        if end_year != None:
            for book in self.bookList:
                if book['publication_year']<= end_year:
                    results_end_year.append(book)
            resultArray.append(results_end_year)

        # Sorts the array of array interms of len, longest to shortest
        sortedResultArray = sorted(resultArray, key=len)

        if len(sortedResultArray) >1 :
            tmp = self.findArrayIntersections(sortedResultArray)
            if sort_by == 'title' :
                return self.sort_by_title(tmp)
            elif sort_by == 'year' :
                return self.sort_by_year(tmp)
            else:
                pass
        return sortedResultArray[0]

    def author(self, author_id):
        ''' Returns the author with the specified ID. (See the BooksDataSource comment for a
            description of how an author is represented.)

            Raises ValueError if author_id is not a valid author ID.
        '''
        for item in self.authorList:
            if item['id'] == author_id:
                return item

        return("Author not found")

    def authors(self, *, book_id=None, search_text=None, start_year=None, end_year=None, sort_by='birth_year'):
        ''' Returns a list of all the authors in this data source matching all of the
            specified non-None criteria.

                book_id - only returns authors of the specified book
                search_text - only returns authors whose first or last names contain
                    (case-insensitively) the search text
                start_year - only returns authors who were alive during or after
                    the specified year
                end_year - only returns authors who were alive during or before
                    the specified year

            Note that parameters with value None do not affect the list of authors returned.
            Thus, for example, calling authors() with no parameters will return JSON for
            a list of all the authors in the data source.

            The list of authors is sorted in an order depending on the sort_by parameter:

                'birth_year' - sorts by birth_year, breaking ties with (case-insenstive) last_name,
                    then (case-insensitive) first_name
                any other value - sorts by (case-insensitive) last_name, breaking ties with
                    (case-insensitive) first_name, then birth_year

            See the BooksDataSource comment for a description of how an author is represented.
        '''
        results_book_id = []
        results_search_text = []
        results_start_year = []
        results_end_year = []

        resultArray = []

        if book_id != None:
            for id in self.link:
                if id['book_id']==book_id:
                    for author in self.authorList:
                        if author['id'] == id['author_id']:
                            results_book_id.append(author)
            resultArray.append(results_book_id)

        if search_text != None:
            for author in self.authorList:
                if author['first_name'].lower().find(search_text.lower())>-1 or author['last_name'].lower().find(search_text.lower())>-1:
                    results_search_text.append(author)
            resultArray.append(results_search_text)

        if start_year != None:
            for author in self.authorList:
                if author['birth_year']>= start_year:
                    results_start_year.append(author)
            resultArray.append(results_start_year)

        if end_year != None:
            if end_year >= self.now.year:
                if sort_by == 'birth_year' :
                    return self.sort_by_birth_year(self.authorList)
                else:
                    return self.sort_by_lastName(self.authorList)

            for author in self.authorList:
                if not author['death_year']== None and author['death_year']<= end_year:
                    results_end_year.append(author)
                elif author['death_year'] == None and end_year<= self.now.year:
                    results_end_year.append(author)
            resultArray.append(results_end_year)

        sortedResultArray = sorted(resultArray, key=len)

        if len(sortedResultArray) >1 :
            tmp = self.findArrayIntersections(sortedResultArray)
            if sort_by == 'birth_year' :
                return self.sort_by_birth_year(tmp)
            else:
                return self.sort_by_lastName(tmp)
        return sortedResultArray[0]

    # Based on JYamada's code
    def sort_by_title(self,array):
        '''
        Uses the fact that sorted is 'stable' to sort the the books by Title first and then year
        '''
        newList = sorted(array, key=lambda k: k['publication_year'])
        newList_ = sorted(newList, key=lambda k: k['title'])
        return newList_

    def sort_by_year(self,array):
        '''
        Uses the fact that sorted is 'stable' to sort the the books by year first and then title
        '''
        newList = sorted(array, key=lambda k: k['title'])
        newList_ = sorted(newList, key=lambda k: k['year'])
        return newList_

    def sort_by_birth_year(self,array):
        '''
        Uses the fact that sorted is 'stable' to sort the the authors in the order --
        birth_year, last_name, first_name
        '''
        newList = sorted(array, key=lambda k: k['first_name'])
        newList_ = sorted(newList, key=lambda k: k['last_name'])
        newList__ = sorted(newList_, key=lambda k: k['birth_year'])
        return newList__

    def sort_by_lastName(self,array):
        '''
        Uses the fact that sorted is 'stable' to sort the the authors in the order --
        last_name, first_name, birth_year
        '''
        newList = sorted(array, key=lambda k: k['birth_year'])
        newList_ = sorted(newList, key=lambda k: k['first_name'])
        newList__ = sorted(newList_, key=lambda k: k['last_name'])
        return newList__

    # Note for my students: The following two methods provide no new functionality beyond
    # what the books(...) and authors(...) methods already provide. But they do represent a
    # category of methods known as "convenience methods". That is, they provide very simple
    # interfaces for a couple very common operations.
    #
    # A question for you: do you think it's worth creating and then maintaining these
    # particular convenience methods? Is books_for_author(17) better than books(author_id=17)?

    def findArrayIntersections(self,sortedResultArray):
        '''
        Finds common elements in the provided array of arraysself.
        Returns an array of common elements
        '''
        results = []
        # Iterates through the shortest array and then searches the rest for intersection.
        for item in sortedResultArray[0]:
            insert = True
            for i in range(1, len(sortedResultArray)):
                if item not in sortedResultArray[i]:
                    insert = False
            if insert:
                results.append(item)
        return results

    def books_for_author(self, author_id):
        ''' Returns a list of all the books written by the author with the specified author ID.
            See the BooksDataSource comment for a description of how an book is represented. '''
        return self.bookList(author_id=author_id)

    def authors_for_book(self, book_id):
        ''' Returns a list of all the authors of the book with the specified book ID.
            See the BooksDataSource comment for a description of how an author is represented. '''
        return self.authorList(book_id=book_id)
